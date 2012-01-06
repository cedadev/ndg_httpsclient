try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='ndg_httpsclient',
    version="0.1.0",
    description='Provides HTTPS for httplib and urllib2 using PyOpenSSL',
    author='Richard Wilkinson',
    long_description=open('README').read(),
    license='BSD - See LICENCE file for details',
    namespace_packages=['ndg'],
    packages=find_packages(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (BSD)',
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
        'console_scripts': ['ndg_httpclient = myproxy.script:main',
                            ],
        }
)
