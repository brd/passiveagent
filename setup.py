from setuptools import setup

setup(
  name='passiveagent',
  version='0.1.9',
  install_requires=['requests'],
  packages=['libpassiveagent'],
  scripts=['passiveagent.py']
)
