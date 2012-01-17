"""unit tests module for ndg.httpsclient.https.HTTPSconnection class

PyOpenSSL utility to make a httplib-like interface suitable for use with 
urllib2
"""
__author__ = "P J Kershaw (STFC)"
__date__ = "06/01/12"
__copyright__ = "(C) 2012 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import logging
logging.basicConfig(level=logging.DEBUG)
import unittest
import socket

from ndg.httpsclient.test import Constants
from ndg.httpsclient.https import HTTPSConnection


class TestHTTPSConnection(unittest.TestCase):
    '''Test ndg HTTPS client HTTPSConnection class'''

    def test01_open(self):
        conn = HTTPSConnection(Constants.HOSTNAME, port=Constants.PORT)
        conn.connect()
        conn.request('GET', '/')
        resp = conn.getresponse()
        print('Response = %s' % resp.read())
        conn.close()

    def test02_open_fails(self):
        conn = HTTPSConnection(Constants.HOSTNAME, port=Constants.PORT2)
        self.failUnlessRaises(socket.error, conn.connect)


if __name__ == "__main__":
    unittest.main()