#! /usr/bin/env python
"""
setup.py for ESSReflReducer

@author: Andrew R. McCluskey (andrew.mccluskey@ess.eu)
"""

# System imports
import io
from os import path
from setuptools import setup, find_packages

PACKAGES = find_packages()

# versioning
from ESSReflReducer import __version__
ISRELEASED = False
VERSION = __version__


THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with io.open(path.join(THIS_DIRECTORY, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

INFO = {
        'name': 'ESSReflReducer',
        'description': 'Reduction for Reflectometry @ ESS',
        'author': 'Andrew R. McCluskey',
        'author_email': 'andrew.mccluskey@ess.eu',
        'packages': PACKAGES,
        'include_package_data': True,
        'setup_requires': ['numpy', 'datetime'],
        'install_requires': ['numpy', 'datetime'],
        'version': VERSION,
        'license': 'MIT',
        'long_description': LONG_DESCRIPTION,
        'long_description_content_type': 'text/markdown',
        'classifiers': ['Development Status :: 4 - Beta',
                        'Intended Audience :: Science/Research',
                        'License :: OSI Approved :: MIT License',
                        'Natural Language :: English',
                        'Operating System :: OS Independent',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.7',
                        'Programming Language :: Python :: 3.8',
                        'Topic :: Scientific/Engineering',
                        'Topic :: Scientific/Engineering :: Chemistry',
                        'Topic :: Scientific/Engineering :: Physics']
        }

####################################################################
# this is where setup starts
####################################################################


def setup_package():
    """
    Runs package setup
    """
    setup(**INFO)


if __name__ == '__main__':
    setup_package()
