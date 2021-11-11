from setuptools import setup

setup(
  name='passiveagent',
  version='0.2.1',
  install_requires=['requests'],
  packages=['libpassiveagent'],
  scripts=['passiveagent.py']
)
