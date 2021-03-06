#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

author_list = ['Céline Durniak', 'Miguel Gonzalez', 'Anders Markvardsen', 'Thomas Farmer']
authors = ', '.join(author_list[:-1]) + ', and ' + author_list[-1]

short = 'Library of models for fitting QENS data'

setup(name='QENSmodels',
      version='0.1.1',
      description=short,
      url='https://github.com/QENSlibrary/QENSmodels',
      author=authors,
      author_email='  ',
      license=open('LICENSE.txt').read(),
      packages=find_packages(),
      install_requires=['scipy', 'numpy', ],
      setup_requires=['flake8'],
      zip_safe=False,)
