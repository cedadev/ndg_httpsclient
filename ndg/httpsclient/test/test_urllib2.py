"""unit tests module for ndg.httpsclient.urllib2_build_opener module

PyOpenSSL utility to make a httplib-like interface suitable for use with 
urllib2
"""
__author__ = "P J Kershaw (STFC)"
__date__ = "06/01/12"
__copyright__ = "(C) 2012 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
from urllib2 import URLError
import unittest

from ndg.httpsclient.test import Constants
from ndg.httpsclient.urllib2_build_opener import build_opener


class Urllib2TestCase(unittest.TestCase):
    """Unit tests for urllib2 functionality"""
    
    def test01_urllib2_build_opener(self):     
        opener = build_opener()
        self.assert_(opener)

    def test02_open(self):
        opener = build_opener()
        res = opener.open(Constants.TEST_URI)
        self.assert_(res)
        print("res = %s" % res.read())

    def test03_open_fails(self):
        opener = build_opener()
        self.failUnlessRaises(URLError, opener.open, Constants.TEST_URI2)
        

if __name__ == "__main__":
    unittest.main()