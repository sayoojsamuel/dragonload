#!/usr/bin/env python3

from setuptools import setup

setup(name='dragonload',
      version='0.1',
      description='Distributed Download Manager for Restricted Networks',
      url='http://sayoojsamuel.github.io',
      author='Sayooj Samuel',
      author_email='sayoojsamuelgreat@gmail.com',
      license='MIT',
      install_requires=["coloredlogs", "tqdm", "requests"],
      packages=['dragonload'],
      zip_safe=False)
