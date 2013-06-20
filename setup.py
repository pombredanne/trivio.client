import os.path
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

README_PATH = os.path.join(HERE, 'README.rst')
try:
    README = open(README_PATH).read()
except IOError:
    README = ''

setup(
  name='trivio',
  packages=find_packages(),
  version='0.2.6',
  description='triv.io command line client',
  long_description=README,
  author='Scott Robertson',
  author_email='scott@triv.io',
  url='http://github.com/trivio/trivio.client',
  classifiers=[
      "Programming Language :: Python",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Development Status :: 3 - Alpha",
      "Environment :: Web Environment",
      "Intended Audience :: Developers",
      "Topic :: Software Development",
  ],
  entry_points = {
    'console_scripts': [
      'trivio = triv.io.client:main',
    ]
  },
  dependency_links = [
    'https://github.com/trivio/leisure/tarball/master#egg=leisure-0.0.4',
    'https://github.com/trivio/codd/tarball/master#egg=codd-0.1.5',
    'https://github.com/trivio/trivio.datasources/tarball/master#egg=trivio.datasources-0.0.2',

  ],
  install_requires=[
    'codd>=0.1.6',
    'leisure',
    'mechanize>=0.2.5',
    'requests>=1.0.4',
    'websocket',
    'python-dateutil==1.5',
    'docopt',
    'schema',
    'virtualenv >= 1.9.1',
    'trivio.datasources >= 0.0.2'
  ],
)
