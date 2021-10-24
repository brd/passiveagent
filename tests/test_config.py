import pytest

from libpassiveagent import config

def test_simple_config():
  c = {}
  c['config_dir'] = 'tests/simple'
  config.read_config(c)
  assert c['nrdp']['parent'] == ['127.0.0.1']
  assert c['nrdp']['token'] == 'foobar'
  assert c['passive checks']['%hostname%|zpool']['command'] == '/usr/local/libexec/nagios/check_zpools -p ALL'
  assert c['passive checks']['%hostname%|zpool']['interval'] == 300

def test_complicated_config():
  c = {}
  c['config_dir'] = 'tests/complicated'
  config.read_config(c)
  assert c['nrdp']['parent'] == ['https://server1.example.org/nrdp', 'https://server2.example.org/nrdp']
  assert c['passive checks']['%hostname%|check1|30']['interval'] == 30
  assert c['passive checks']['%hostname%|check1|30']['command'] == '/usr/local/libexec/nagios/check_load -c 75'
  # %HOSTNAME%|dns|60 = plugins/check_dns/-H/_healthcheck.corp.care2.com/-q/TXT/-t/5:3
  assert c['passive checks']['%hostname%|dns|60']['command'] == '/usr/local/libexec/nagios/check_dig -H _healthcheck.corp.care2.com -q TXT -t 5:3'

def test_check_command():
  assert config.check_command('/bin/ls') == '/bin/ls'
  assert config.check_command('/bin/ls -F') == '/bin/ls -F'
  assert config.check_command('/bin/ls/-F') == '/bin/ls -F'
  assert config.check_command('/bin/ls/-a/-l') == '/bin/ls -a -l'
