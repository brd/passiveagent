from setuptools import setup

setup(
  name='passiveagent',
  version='0.2.2',
  install_requires=['requests'],
  packages=['libpassiveagent'],
  scripts=['passiveagent.py']
)
