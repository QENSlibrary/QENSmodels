try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

author_list = ['Céline Durniak', 'Miguel Gonzalez', 'Anders Markvardsen']
authors = ', '.join(author_list[:-1]) + ', and ' + author_list[-1]

short = 'Library of models for fitting QENS data'

setup(name='QENSmodels',
      version='0.1',
      description=short,
      url='https://github.com/QENSlibrary/QENSmodels',
      author=authors,
      author_email='to be added',
      license=open('LICENSE.txt').read(),
      packages=['QENSmodels'],
      install_requires=['scipy', 'numpy', 'flake8',],
      zip_safe=False,)
