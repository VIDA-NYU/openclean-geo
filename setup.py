# This file is part of the Data Cleaning Library (openclean).
#
# Copyright (C) 2018-2021 New York University.
#
# openclean is released under the Revised BSD License. See file LICENSE for
# full license details.

"""Required packages for install, test, docs, and tests."""

import os
import re

from setuptools import setup, find_packages


install_requires = [
    'openclean-core>=0.3.0',
    'Shapely>=1.7.1'
]

tests_require = [
    'coverage>=5.0',
    'pytest',
    'pytest-cov'
]

dev_require = ['flake8', 'python-language-server'] + tests_require


extras_require = {
    'docs': [
        'Sphinx',
        'sphinx-rtd-theme'
    ],
    'tests': tests_require,
    'dev': dev_require
}


# Get the version string from the version.py file in the openclean_geo package.
# Based on:
# https://stackoverflow.com/questions/458550
with open(os.path.join('openclean_geo', 'version.py'), 'rt') as f:
    filecontent = f.read()
match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", filecontent, re.M)
if match is not None:
    version = match.group(1)
else:
    raise RuntimeError('unable to find version string in %s.' % (filecontent,))


# Get long project description text from the README.rst file
with open('README.rst', 'rt') as f:
    readme = f.read()


setup(
    name='openclean-geo',
    version=version,
    description='Geo-Spatial extension for the open data cleaning library',
    long_description=readme,
    long_description_content_type='text/x-rst',
    keywords='data cleaning',
    url='https://github.com/VIDA-NYU/openclean-geo',
    author='Heiko Mueller',
    author_email='heiko.muller@gmail.com',
    license_file='LICENSE',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    extras_require=extras_require,
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python'
    ]
)
