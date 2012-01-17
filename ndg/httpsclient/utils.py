import cookielib
import httplib
import logging
from optparse import OptionParser
import os
import urllib2
from urllib2 import HTTPHandler
    
import urlparse

from ndg.httpsclient.urllib2_build_opener import build_opener
from ndg.httpsclient.https import HTTPSContextHandler
from ndg.httpsclient import ssl_context_util


class URLFetchError(Exception):
    """Error fetching content from URL"""
    

def fetch_from_url(url, config):
    """Returns data retrieved from a URL.
    @param url: URL to attempt to open
    @param config: SSL context configuration
    @type config: Configuration
    @return data retrieved from URL or None
    """
    return_code, return_message, response = open_url(url, config)
    if return_code and return_code == httplib.OK:
        return_data = response.read()
        response.close()
        return return_data
    else:
        raise URLFetchError(return_message)

def fetch_from_url_to_file(url, config, output_file):
    """Writes data retrieved from a URL to a file.
    @param url: URL to attempt to open
    @param config: SSL context configuration
    @type config: Configuration
    @param output_file: output file
    @return: tuple (
        returned HTTP status code or 0 if an error occurred
        returned message
        boolean indicating whether access was successful)
    """
    return_code, return_message, response = open_url(url, config)
    if return_code == httplib.OK:
        return_data = response.read()
        response.close()
        outfile = open(output_file, "w")
        outfile.write(return_data)
        outfile.close()
    return return_code, return_message, return_code == httplib.OK


def open_url(url, config):
    """Attempts to open a connection to a specified URL.
    @param url: URL to attempt to open
    @param config: SSL context configuration
    @type config: Configuration
    @return: tuple (
        returned HTTP status code or 0 if an error occurred
        returned message or error description
        response object)
    """
    debuglevel = 1 if config.debug else 0

    # Set up handlers for URL opener.
    cj = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cj)

    handlers = [cookie_handler]

    if config.debug:
        http_handler = HTTPHandler(debuglevel=debuglevel)
        https_handler = HTTPSContextHandler(config.ssl_context, 
                                            debuglevel=debuglevel)
        handlers.extend([http_handler, https_handler])

    # Explicitly remove proxy handling if the host is one listed in the value of
    # the no_proxy environment variable because urllib2 does use proxy settings 
    # set via http_proxy and https_proxy, but does not take the no_proxy value 
    # into account.
    if not _should_use_proxy(url):
        handlers.append(urllib2.ProxyHandler({}))
        if config.debug:
            print "Not using proxy"

    opener = build_opener(config.ssl_context, *handlers)

    # Open the URL and check the response.
    return_code = 0
    return_message = ''
    response = None
    try:
        response = opener.open(url)
        if response.url == url:
            return_message = response.msg
            return_code = response.code
        else:
            return_message = 'Redirected (%s  %s)' % response.code, response.url
        if config.debug:
            for index, cookie in enumerate(cj):
                print index, '  :  ', cookie        
    except urllib2.HTTPError, exc:
        return_code = exc.code
        return_message = "Error: %s" % exc.msg
        if config.debug:
            print exc.code, exc.msg
    except Exception, exc:
        return_message = "Error: %s" % exc.__str__()
        if config.debug:
            print exc.__class__, exc.__str__()
    return (return_code, return_message, response)


def _should_use_proxy(url):
    """Determines whether a proxy should be used to open a connection to the 
    specified URL, based on the value of the no_proxy environment variable.
    @param url: URL
    @type url: basestring
    """
    no_proxy = os.environ.get('no_proxy', '')

    urlObj = urlparse.urlparse(url)
    for np in [h.strip() for h in no_proxy.split(',')]:
        if urlObj.hostname == np:
            return False

    return True


class Configuration(object):
    """Checker configuration.
    """
    def __init__(self, ssl_context, debug):
        """
        @param ssl_context: SSL context to use with this configuration
        @type ssl_context: OpenSSL.SSL.Contex        @param debug: if True, output debugging information
        @type debug: boo
        """
        self.ssl_context = ssl_context
        self.debug = debug


def main():
    '''Utility to fetch data using HTTP or HTTPS GET from a specified URL.
    '''
    parser = OptionParser(usage="%prog [options] url")
    parser.add_option("-k", "--private-key", dest="key_file", metavar="FILE",
                      default=None,
                      help="Private key file.")
    parser.add_option("-c", "--certificate", dest="cert_file", metavar="FILE",
                      default=os.path.expanduser("~/credentials.pem"),
                      help="Certificate file.")
    parser.add_option("-t", "--ca-certificate-dir", dest="ca_dir", 
                      metavar="PATH",
                      default=None,
                      help="Trusted CA certificate file directory.")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", 
                      default=False,
                      help="Print debug information.")
    parser.add_option("-f", "--fetch", dest="output_file", metavar="FILE",
                      default=None, help="Output file.")
    parser.add_option("-n", "--no-verify-peer", action="store_true", 
                      dest="no_verify_peer", default=False,
                      help="Skip verification of peer certificate.")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect number of arguments")

    url = args[0]
    
    if options.key_file and os.path.exists(options.key_file):
        key_file = options.key_file
    else:
        key_file = None
    
    if options.cert_file and os.path.exists(options.cert_file):
        cert_file = options.cert_file
    else:
        cert_file = None
    
    if options.ca_dir and os.path.exists(options.ca_dir):
        ca_dir = options.ca_dir 
    else:
        ca_dir = None
        
    verify_peer = not options.no_verify_peer
    
    # If a private key file is not specified, the key is assumed to be stored in 
    # the certificate file.
    ssl_context = ssl_context_util.make_ssl_context(key_file,
                                                    cert_file,
                                                    None,
                                                    ca_dir,
                                                    verify_peer, 
                                                    url)

    config = Configuration(ssl_context, options.debug)
    if options.output_file:
        return_code, return_message = fetch_from_url_to_file(url, 
                                                      config,
                                                      options.output_file)[:2]
        raise SystemExit(return_code, return_message)
    else:
        data = fetch_from_url(url, config)
        print(data)


if __name__=='__main__':
    logging.basicConfig()
    main()
