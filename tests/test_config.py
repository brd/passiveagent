import pytest
import configparser

import config

def test_simple_config():
  c = config.read_config('tests/simple')
  assert c['nrdp']['parent'] == '127.0.0.1'
  assert c['nrdp']['token'] == 'foobar'
  assert c['passive checks']['%%HOSTNAME%%|ZPOOL'] == 'check_zpool.sh -p ALL'
