try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='urllib2pyopenssl',
    version="0.1.0",
    description='Provides HTTPS with urllib2 using PyOpenSSL',
    author='Richard Wilkinson',
    long_description=open('README').read(),
    license='BSD - See LICENCE file for details',
    namespace_packages=['ndg'],
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
#            'urllib2pyopenssl_get = urllib2pyopenssl.get:main'
            ]
        }
)
