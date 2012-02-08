try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

_long_description = '''
This is a HTTPS client implementation for httplib and urllib2 based on 
PyOpenSSL.  PyOpenSSL provides a more fully featured SSL implementation over the
default provided with Python and importantly enables full verification of the
SSL peer. 

Prerequisites
=============
This has been developed and tested for Python 2.6 and 2.7 with pyOpenSSL 0.13.  
Note that proxy support is only available from Python 2.6.2 onwards.  pyasn1 is 
required for correct SSL verification with subjectAltNames.

Installation
============
Installation can be performed using easy_install or pip.  

Running ndg_httpclient
======================
A simple script for fetching data using HTTP or HTTPS GET from a specified URL.
 
Parameter::
    url                   The URL of the resource to be fetched

Options::
    -h, --help            Show help message and exit.
    -c FILE, --certificate=FILE
                          Certificate file - defaults to $HOME/credentials.pem
    -k FILE, --private-key=FILE
                          Private key file - defaults to the certificate file
    -t DIR, --ca-certificate-dir=DIR
                          Trusted CA certificate file directory.
    -d, --debug           Print debug information - this may be useful in 
                          solving problems with HTTP or HTTPS access to a 
                          server.
    -f FILE, --fetch=FILE Output file
    -n, --no-verify-peer  Skip verification of peer certificate.
'''
    
setup(
    name='ndg_httpsclient',
    version="0.2.0",
    description='Provides enhanced HTTPS support for httplib and urllib2 using '
                'PyOpenSSL',
    author='Richard Wilkinson and Philip Kershaw',
    author_email='Philip.Kershaw@stfc.ac.uk',
    url='http://ndg-security.ceda.ac.uk/wiki/ndg_httpsclient/',
    long_description=_long_description,
    license='BSD - See LICENCE file for details',
    namespace_packages=['ndg'],
    packages=find_packages(),
    package_dir={'ndg.httpsclient': 'ndg/httpsclient'},
    package_data={
        'ndg.httpsclient': [
            'test/README', 
            'test/scripts/*.sh',
            'test/pki/localhost.*',
            'test/pki/ca/*.0'
            ],
    },
    install_requires = ['PyOpenSSL'],
    extras_require = {'subjectAltName_support': 'pyasn1'},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe = False,
    entry_points = {
        'console_scripts': ['ndg_httpclient = ndg.httpsclient.utils:main',
                            ],
        }
)
