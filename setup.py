#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='cmdbot',
    version='1.0.2',
    packages=['cmdbot'],
    url='https://github.com/brunobord/cmdbot/',
    author="Bruno Bord",
    author_email='bruno@jehaisleprintemps.net',
    license="Public Domain (WTFPL)",
    platforms='any',
    description="An IRC Bot with a `cmd` attitude",
    long_description=long_description,
)
