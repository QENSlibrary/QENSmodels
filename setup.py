#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

author_list = ['Céline Durniak', 'Miguel Gonzalez', 'Anders Markvardsen', 'Thomas Farmer']
authors = ', '.join(author_list[:-1]) + ', and ' + author_list[-1]

short = 'Library of models for fitting QENS data'

packages = ['QENSmodels']

setup(name='QENSmodels',
      version='0.1.2',
      description=short,
      url='https://github.com/QENSlibrary/QENSmodels',
      author=authors,
      author_email='  ',
      license=open('LICENSE.txt').read(),
      packages=packages,
      python_requires=">=3.7,<3.11",
      install_requires=['scipy', 'numpy', ],
      setup_requires=['flake8'],
      tests_require=['pytest'],
      zip_safe=False,)
