'''
Created on Jan 5, 2012

@author: philipkershaw
'''
import unittest
from ndg.httpsclient.urllib2_build_opener import urllib2_build_opener
from ndg.httpsclient.https import HTTPSConnection


class Urllib2PyOpenSslTestCase(unittest.TestCase):
    """Unit tests for PyOpenSSL HTTPS interface for urllib2"""
    TEST_URI = 'https://localhost:4443'
    
    def test01_httpsconnection(self):
        conn = HTTPSConnection('localhost', port=4443)
        conn.connect()
        
        conn.close()
        
    def test02_urllib2_build_opener(self):     
        opener = urllib2_build_opener()
        self.assert_(opener)

    def test03_open(self):
        opener = urllib2_build_opener()
        res = opener.open(self.__class__.TEST_URI)
        self.assert_(res)
        print("res = %s" % res.read())

if __name__ == "__main__":
    unittest.main()