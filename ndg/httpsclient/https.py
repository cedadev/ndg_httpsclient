"""urllib2pyopenssl HTTPS module containing PyOpenSSL implementation of
httplib.HTTPSConnection

PyOpenSSL utility to make a httplib-like interface suitable for use with 
urllib2
"""
__author__ = "P J Kershaw (STFC)"
__date__ = "09/12/11"
__copyright__ = "(C) 2012 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import logging
import socket
from httplib import HTTPConnection, HTTPS_PORT
from urllib2 import AbstractHTTPHandler

from OpenSSL import SSL

from urllib2pyopenssl.ssl_socket import SSLSocket

log = logging.getLogger(__name__)


class HTTPSConnection(HTTPConnection):
    """This class allows communication via SSL using PyOpenSSL.
    It is based on httplib.HTTPSConnection, modified to use PyOpenSSL.

    Note: This uses the constructor inherited from HTTPConnection to allow it to
    be used with httplib and HTTPSContextHandler. To use the class directly with
    an SSL context set ssl_context after construction.
    @cvar default_port: default port for this class (443)
    @type default_port: int
    """
    default_port = HTTPS_PORT

    def __init__(self, host, port=None, strict=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        HTTPConnection.__init__(self, host, port, strict, timeout)
        if not hasattr(self, 'ssl_context'):
            self.ssl_context = None

    def connect(self):
        """Create SSL socket and connect to peer
        """ 
        if getattr(self, 'ssl_context', None):
            if not isinstance(self.ssl_context, SSL.Context):
                raise TypeError('Expecting OpenSSL.SSL.Context type for "'
                                'ssl_context" keyword; got %r instead' %
                                self.ssl_context)
            ssl_context = self.ssl_context
        else:
            ssl_context = SSL.Context(SSL.SSLv23_METHOD)

        sock = socket.create_connection((self.host, self.port), self.timeout)
        if getattr(self, '_tunnel_host', None):
            self.sock = sock
            self._tunnel()
        self.sock = SSLSocket(ssl_context, sock)
        # Go to client mode.
        self.sock.set_connect_state()

    def close(self):
        """Close socket and shut down SSL connection"""
        self.sock.close()
        

class HTTPSContextHandler(AbstractHTTPHandler):
    '''HTTPS handler that provides allows a SSL context to be set for the SSL
    connections.
    '''
    https_request = AbstractHTTPHandler.do_request_

    def __init__(self, ssl_context, debuglevel=0):
        """
        @param ssl_context - SSL context
        @param debuglevel - debug level for HTTPSHandler
        """
        AbstractHTTPHandler.__init__(self, debuglevel)

        if ssl_context is not None:
            if not isinstance(ssl_context, SSL.Context):
                raise TypeError('Expecting OpenSSL.SSL.Context type for "'
                                'ssl_context" keyword; got %r instead' %
                                ssl_context)
            self.ssl_context = ssl_context
        else:
            self.ssl_context = SSL.Context(SSL.SSLv23_METHOD)

    def https_open(self, req):
        """Opens HTTPS request
        @param req - HTTP request
        @return HTTP Response object
        """
        # Make a custom class extending HTTPSConnection, with the SSL context
        # set as a class variable so that it is available to the connect method.
        customHTTPSContextConnection = type('CustomHTTPSContextConnection',
                                            (HTTPSConnection, object),
                                            {'ssl_context': self.ssl_context})
        return self.do_open(customHTTPSContextConnection, req)
