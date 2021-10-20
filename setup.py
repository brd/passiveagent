from setuptools import setup

setup(
  name='passiveagent',
  version='0.2.0',
  install_requires=['requests'],
  packages=['libpassiveagent'],
  scripts=['passiveagent.py']
)
