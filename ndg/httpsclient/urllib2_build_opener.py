"""PyOpenSSL utilities including HTTPSSocket class which wraps PyOpenSSL
SSL connection into a httplib-like interface suitable for use with urllib2
"""
__author__ = "P J Kershaw"
__date__ = "21/12/10"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id: pyopenssl.py 7929 2011-08-16 16:39:13Z pjkersha $'

import logging
from urllib2 import (OpenerDirector, ProxyHandler, UnknownHandler, HTTPHandler,
                     HTTPDefaultErrorHandler, HTTPRedirectHandler,
                     FTPHandler, FileHandler, HTTPErrorProcessor)

from urllib2pyopenssl.https import HTTPSContextHandler

log = logging.getLogger(__name__)

# Copied from urllib2 with modifications for ssl
def urllib2_build_opener(ssl_context=None, *handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP and FTP.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """
    import types
    def isclass(obj):
        return isinstance(obj, types.ClassType) or hasattr(obj, "__bases__")

    opener = OpenerDirector()
    default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
                       HTTPDefaultErrorHandler, HTTPRedirectHandler,
                       FTPHandler, FileHandler, HTTPErrorProcessor]
    check_classes = list(default_classes)
    check_classes.append(HTTPSContextHandler)
    skip = []
    for klass in check_classes:
        for check in handlers:
            if isclass(check):
                if issubclass(check, klass):
                    skip.append(klass)
            elif isinstance(check, klass):
                skip.append(klass)

    for klass in default_classes:
        if klass not in skip:
            opener.add_handler(klass())

    # Add the HTTPS handler with ssl_context
    if HTTPSContextHandler not in skip:
        opener.add_handler(HTTPSContextHandler(ssl_context))

    for h in handlers:
        if isclass(h):
            h = h()
        opener.add_handler(h)

    return opener
