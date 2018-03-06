try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


short = 'Library of models for fitting QENS data'

setup(name='QENSlibrary',
      version='0.1',
      description=short,
      url='https://github.com/QENSlibrary',
      author='to be added',
      author_email='to be added',
      license=open('LICENSE.txt').read(),
      packages=['QENSmodels'],
      zip_safe=False)
