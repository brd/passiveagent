import pytest

import config

def test_simple_config():
  c = config.read_config('tests/simple')
  assert c['nrdp']['parent'] == ['127.0.0.1']
  assert c['nrdp']['token'] == 'foobar'
  assert c['passive checks']['%%hostname%%|zpool']['command'] == 'check_zpools -p ALL'
  assert c['passive checks']['%%hostname%%|zpool']['interval'] == 300

def test_complicated_config():
  c = config.read_config('tests/complicated')
  assert c['nrdp']['parent'] == ['https://server1.example.org/nrdp', 'https://server2.example.org/nrdp']
  assert c['passive checks']['%%hostname%%|check1|30']['interval'] == 30
