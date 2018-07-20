try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

NAMESPACE_PKGS = ['ndg']

with open('README.md') as f:
    _long_description = f.read()

setup(
    name='ndg_httpsclient',
    version="0.5.1",
    description='Provides enhanced HTTPS support for httplib and urllib2 using '
                'PyOpenSSL',
    author='Richard Wilkinson and Philip Kershaw',
    author_email='Philip.Kershaw@stfc.ac.uk',
    url='https://github.com/cedadev/ndg_httpsclient/',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    license='BSD - See ndg/httpsclient/LICENCE file for details',
    packages=find_packages(),
    package_data={
        'ndg.httpsclient': [
            'LICENSE',
            'test/README',
            'test/scripts/*.sh',
            'test/pki/localhost.*',
            'test/pki/ca/*.0'
            ],
    },
    install_requires=['PyOpenSSL', 'pyasn1>=0.1.1'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': ['ndg_httpclient = ndg.httpsclient.utils:main',
                            ],
        }
)
