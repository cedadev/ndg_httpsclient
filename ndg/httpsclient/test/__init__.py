"""unit tests package for urllib2pyopenssl

PyOpenSSL utility to make a httplib-like interface suitable for use with 
urllib2
"""
__author__ = "P J Kershaw (STFC)"
__date__ = "05/01/12"
__copyright__ = "(C) 2012 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
class Constants(object):
    PORT = 4443
    HOSTNAME = 'localhost'
    TEST_URI = 'https://%s:%d' % (HOSTNAME, PORT)