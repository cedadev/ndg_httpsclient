'''
Created on 12 Jan 2012

@author: rwilkinson
'''
import base64
import socket
import urlparse
from urllib import unquote, addinfourl
from urllib2 import _parse_proxy, URLError, HTTPError
from urllib2 import (AbstractHTTPHandler as _AbstractHTTPHandler,
                     BaseHandler as _BaseHandler,
                     HTTPRedirectHandler as _HTTPRedirectHandler,
                     Request as _Request,
                     OpenerDirector as _OpenerDirector)

from ndg.httpsclient.httplib_proxy import HTTPConnection


class Request(_Request):

    def __init__(self, *args, **kw):
        _Request.__init__(self, *args, **kw)
        self._tunnel_host = None

    def set_proxy(self, host, type):
        if self.type == 'https' and not self._tunnel_host:
            self._tunnel_host = self.host
        else:
            self.type = type
            self.__r_host = self.__original
        self.host = host


class BaseHandler(_BaseHandler):
    def proxy_open(self, req, proxy, type):
        if req.get_type() == 'https':
            orig_type = req.get_type()
            proxy_type, user, password, hostport = _parse_proxy(proxy)
            if proxy_type is None:
                proxy_type = orig_type
            if user and password:
                user_pass = '%s:%s' % (unquote(user), unquote(password))
                creds = base64.b64encode(user_pass).strip()
                req.add_header('Proxy-authorization', 'Basic ' + creds)
            hostport = unquote(hostport)
            req.set_proxy(hostport, proxy_type)
            # let other handlers take care of it
            return None
        else:
            return _BaseHandler.proxy_open(self, req, proxy, type)

class AbstractHTTPHandler(_AbstractHTTPHandler):
    def do_open(self, http_class, req):
        """Return an addinfourl object for the request, using http_class.

        http_class must implement the HTTPConnection API from httplib.
        The addinfourl return value is a file-like object.  It also
        has methods and attributes including:
            - info(): return a mimetools.Message object for the headers
            - geturl(): return the original request URL
            - code: HTTP status code
        """
        host = req.get_host()
        if not host:
            raise URLError('no host given')

        h = http_class(host, timeout=req.timeout) # will parse host:port
        h.set_debuglevel(self._debuglevel)

        headers = dict(req.headers)
        headers.update(req.unredirected_hdrs)
        # We want to make an HTTP/1.1 request, but the addinfourl
        # class isn't prepared to deal with a persistent connection.
        # It will try to read all remaining data from the socket,
        # which will block while the server waits for the next request.
        # So make sure the connection gets closed after the (only)
        # request.
        headers["Connection"] = "close"
        headers = dict(
            (name.title(), val) for name, val in headers.items())

        if not hasattr(req, '_tunnel_host'):
            pass
        
        if req._tunnel_host:
            h.set_tunnel(req._tunnel_host)
        try:
            h.request(req.get_method(), req.get_selector(), req.data, headers)
            r = h.getresponse()
        except socket.error, err: # XXX what error?
            raise URLError(err)

        # Pick apart the HTTPResponse object to get the addinfourl
        # object initialized properly.

        # Wrap the HTTPResponse object in socket's file object adapter
        # for Windows.  That adapter calls recv(), so delegate recv()
        # to read().  This weird wrapping allows the returned object to
        # have readline() and readlines() methods.

        # XXX It might be better to extract the read buffering code
        # out of socket._fileobject() and into a base class.

        r.recv = r.read
        fp = socket._fileobject(r, close=True)

        resp = addinfourl(fp, r.msg, req.get_full_url())
        resp.code = r.status
        resp.msg = r.reason
        return resp


class HTTPHandler(AbstractHTTPHandler):

    def http_open(self, req):
        return self.do_open(HTTPConnection, req)

    http_request = AbstractHTTPHandler.do_request_

#if hasattr(httplib, 'HTTPS'):
#    class HTTPSHandler(AbstractHTTPHandler):
#
#        def https_open(self, req):
#            return self.do_open(httplib.HTTPSConnection, req)
#
#        https_request = AbstractHTTPHandler.do_request_


class HTTPRedirectHandler(BaseHandler):
    # maximum number of redirections to any single URL
    # this is needed because of the state that cookies introduce
    max_repeats = 4
    # maximum total number of redirections (regardless of URL) before
    # assuming we're in a loop
    max_redirections = 10

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return a Request or None in response to a redirect.

        This is called by the http_error_30x methods when a
        redirection response is received.  If a redirection should
        take place, return a new Request to allow http_error_30x to
        perform the redirect.  Otherwise, raise HTTPError if no-one
        else should try to handle this url.  Return None if you can't
        but another Handler might.
        """
        m = req.get_method()
        if (code in (301, 302, 303, 307) and m in ("GET", "HEAD")
            or code in (301, 302, 303) and m == "POST"):
            # Strictly (according to RFC 2616), 301 or 302 in response
            # to a POST MUST NOT cause a redirection without confirmation
            # from the user (of urllib2, in this case).  In practice,
            # essentially all clients do redirect in this case, so we
            # do the same.
            # be conciliant with URIs containing a space
            newurl = newurl.replace(' ', '%20')
            newheaders = dict((k,v) for k,v in req.headers.items()
                              if k.lower() not in ("content-length", "content-type")
                             )
            return Request(newurl,
                           headers=newheaders,
                           origin_req_host=req.get_origin_req_host(),
                           unverifiable=True)
        else:
            raise HTTPError(req.get_full_url(), code, msg, headers, fp)

    # Implementation note: To avoid the server sending us into an
    # infinite loop, the request object needs to track what URLs we
    # have already seen.  Do this by adding a handler-specific
    # attribute to the Request object.
    def http_error_302(self, req, fp, code, msg, headers):
        # Some servers (incorrectly) return multiple Location headers
        # (so probably same goes for URI).  Use first header.
        if 'location' in headers:
            newurl = headers.getheaders('location')[0]
        elif 'uri' in headers:
            newurl = headers.getheaders('uri')[0]
        else:
            return

        # fix a possible malformed URL
        urlparts = urlparse.urlparse(newurl)
        if not urlparts.path:
            urlparts = list(urlparts)
            urlparts[2] = "/"
        newurl = urlparse.urlunparse(urlparts)

        newurl = urlparse.urljoin(req.get_full_url(), newurl)

        # For security reasons we do not allow redirects to protocols
        # other than HTTP, HTTPS or FTP.
        newurl_lower = newurl.lower()
        if not (newurl_lower.startswith('http://') or
                newurl_lower.startswith('https://') or
                newurl_lower.startswith('ftp://')):
            raise HTTPError(newurl, code,
                            msg + " - Redirection to url '%s' is not allowed" %
                            newurl,
                            headers, fp)

        # XXX Probably want to forget about the state of the current
        # request, although that might interact poorly with other
        # handlers that also use handler-specific request attributes
        new = self.redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return

        # loop detection
        # .redirect_dict has a key url if url was previously visited.
        if hasattr(req, 'redirect_dict'):
            visited = new.redirect_dict = req.redirect_dict
            if (visited.get(newurl, 0) >= self.max_repeats or
                len(visited) >= self.max_redirections):
                raise HTTPError(req.get_full_url(), code,
                                self.inf_msg + msg, headers, fp)
        else:
            visited = new.redirect_dict = req.redirect_dict = {}
        visited[newurl] = visited.get(newurl, 0) + 1

        # Don't close the fp until we are sure that we won't use it
        # with HTTPError.
        fp.read()
        fp.close()

        return self.parent.open(new, timeout=req.timeout)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

    inf_msg = "The HTTP server returned a redirect error that would " \
              "lead to an infinite loop.\n" \
              "The last 30x error message was:\n"
              

class OpenerDirector(_OpenerDirector):
    def open(self, fullurl, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        # accept a URL or a Request object
        if isinstance(fullurl, basestring):
            req = Request(fullurl, data)
        else:
            req = fullurl
            if data is not None:
                req.add_data(data)

        req.timeout = timeout
        protocol = req.get_type()

        # pre-process request
        meth_name = protocol+"_request"
        for processor in self.process_request.get(protocol, []):
            meth = getattr(processor, meth_name)
            req = meth(req)

        response = self._open(req, data)
        
        # post-process response
        meth_name = protocol+"_response"
        for processor in self.process_response.get(protocol, []):
            meth = getattr(processor, meth_name)
            response = meth(req, response)

        return response