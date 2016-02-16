#!/usr/bin/env python

from distutils.core import setup

setup(name='django-lbos',
      version='1.0',
      install_requires = ['ncbi-lbos>=1.0.4', 'python-decouple>=3.0'],
      description='Announcer for Django apps',
      author_email='python-core@ncbi.nlm.nih.gov',
      url='https://stash.ncbi.nlm.nih.gov/projects/PY/repos',
      scripts=['register.py'],
      )

