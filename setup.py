#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name = 'sc2profile',
    version = version,
    description = 'Python starcraft 2 profile fetcher',
    author = 'Fabien Reboia',
    author_email = 'srounet@gmail.com',
    maintainer = 'Fabien Reboia',
    license = 'Bearware',
    url = 'http://github.com/srounet/sc2profile',
    packages = find_packages(exclude=['tests']),
    install_requires = [
        'lxml'
    ],
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
)
