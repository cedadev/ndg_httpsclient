'''
Created on Jan 5, 2012

@author: philipkershaw
'''
import unittest
from ndg.httpsclient.urllib2_build_opener import build_opener


class Urllib2PyOpenSslTestCase(unittest.TestCase):
    """Unit tests for PyOpenSSL HTTPS interface for urllib2"""
    TEST_URI = 'https://localhost:4443'
    
    def test01_urllib2_build_opener(self):     
        opener = build_opener()
        self.assert_(opener)

    def test02_open(self):
        opener = build_opener()
        res = opener.open(self.__class__.TEST_URI)
        self.assert_(res)
        print("res = %s" % res.read())

if __name__ == "__main__":
    unittest.main()