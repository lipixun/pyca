# encoding=utf8
# The setup file

import sys
import os.path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import calib

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [ x.strip() for x in open('requirements.txt').readlines() ]

setup(
    name = 'calib',
    version = calib.__version__,
    author = 'lipixun',
    author_email = 'lipixun@outlook.com',
    url = 'https://github.com/lipixun/pyca',
    packages = [ 'calib' ],
    package_data = { 'calib': [ 'openssl.config.template' ] },
    install_requires = requirements,
    license = 'LICENSE',
    description = 'Certificate Authority Lib & Tools',
    long_description = open('README.md').read(),
    keywords = [ 'python', 'ca', 'certificate', 'openssl' ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)

