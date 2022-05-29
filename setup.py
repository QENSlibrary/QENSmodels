#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
import os

author_list = ['Céline Durniak', 'Miguel Gonzalez', 'Anders Markvardsen', 'Thomas Farmer']
authors = ', '.join(author_list[:-1]) + ', and ' + author_list[-1]

short = 'Library of models for fitting QENS data'

packages = ['QENSmodels']

# get version number
here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, "QENSmodels", "_version.py")

pkg_vars = {}

with open(version_path) as fp:
    exec(fp.read(), pkg_vars)

found_version = pkg_vars['__version__']
print("Version read from file:", found_version)


setup(name='QENSmodels',
      version=found_version,
      description=short,
      url='https://github.com/QENSlibrary/QENSmodels',
      author=authors,
      author_email='  ',
      license=open('LICENSE.txt').read(),
      python_requires=">=3.7,<3.11",
      packages=packages,
      install_requires=['scipy', 'numpy', ],
      setup_requires=['flake8'],
      zip_safe=False,)
