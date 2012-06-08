#!/usr/bin/env python
import os
from distutils.core import setup
curdir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(curdir, 'README.rst')) as fd:
    long_description = fd.read()

setup(
    name='cmdbot',
    version='1.0.4',
    packages=['cmdbot'],
    url='https://github.com/brunobord/cmdbot/',
    author="Bruno Bord",
    author_email='bruno@jehaisleprintemps.net',
    license="Public Domain (WTFPL)",
    platforms='any',
    description="An IRC Bot with a `cmd` attitude",
    long_description=long_description,
    install_requires=['argparse']
)
