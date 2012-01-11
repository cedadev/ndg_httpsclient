'''
Created on Jan 6, 2012

@author: philipkershaw
'''
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