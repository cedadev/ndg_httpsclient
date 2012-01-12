'''
Created on Jan 11, 2012

@author: philipkershaw
'''
import socket
from httplib import HTTPConnection as _HTTPConnection
from httplib import HTTPException

# maximal line length when calling readline().
_MAXLINE = 65536

class LineTooLong(HTTPException):
    def __init__(self, line_type):
        HTTPException.__init__(self, "got more than %d bytes when reading %s"
                                     % (_MAXLINE, line_type))
        

class HTTPConnection(_HTTPConnection):
    NDG_HTTPSCLIENT = True
    
    def __init__(self, *arg, **kwarg):
        self._tunnel_host = None
        self._tunnel_port = None
        self._tunnel_headers = {}

        _HTTPConnection.__init__(self, *arg, **kwarg)
        
    def set_tunnel(self, host, port=None, headers=None):
        """ Sets up the host and the port for the HTTP CONNECT Tunnelling.

        The headers argument should be a mapping of extra HTTP headers
        to send with the CONNECT request.
        """
        self._tunnel_host = host
        self._tunnel_port = port
        if headers:
            self._tunnel_headers = headers
        else:
            self._tunnel_headers.clear()

    def _tunnel(self):
        self._set_hostport(self._tunnel_host, self._tunnel_port)
        self.send("CONNECT %s:%d HTTP/1.0\r\n" % (self.host, self.port))
        for header, value in self._tunnel_headers.iteritems():
            self.send("%s: %s\r\n" % (header, value))
        self.send("\r\n")
        response = self.response_class(self.sock, strict = self.strict,
                                       method = self._method)
        (version, code, message) = response._read_status()

        if code != 200:
            self.close()
            raise socket.error("Tunnel connection failed: %d %s" % (code,
                                                            message.strip()))
        while True:
            line = response.fp.readline(_MAXLINE + 1)
            if len(line) > _MAXLINE:
                raise LineTooLong("header line")
            if line == '\r\n': break
            
    def connect(self):
        """Connect to the host and port specified in __init__."""
        _HTTPConnection.connect(self)

        if self._tunnel_host:
            self._tunnel()
