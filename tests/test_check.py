import pytest
import os

from libpassiveagent import check

def test_check_check():
  config = {}
  config['plugin directives'] = {}
  config['plugin directives']['plugin_path'] = '/usr/local/libexec/nagios'
  config['passive checks'] = {}
  config['passive checks']['%HOSTNAME%|ZPOOL'] = 'check_zpools -p ALL'
  check.check_check(config)

def test_run_check_bad_path():
  with pytest.raises(FileNotFoundError) as execinfo:
    c = {}
    pc = 0
    c['passive checks'] = {}
    c['passive checks'][pc] = {}
    c['passive checks'][pc]['command'] = '/bin/foobar'
    check.run_check(c, pc, False)

def test_run_check_exit_1():
  c = {}
  pc = 0
  c['passive checks'] = {}
  c['passive checks'][pc] = {}
  c['passive checks'][pc]['command'] = '/bin/ls lkjsdlfjasdfljsalkdajfjl'
  test = check.run_check(c, pc, False)
  assert test['code'] == 1
  assert test['stdout'] == ""
  assert test['stderr'] == "ls: lkjsdlfjasdfljsalkdajfjl: No such file or directory"

def test_run_check_exit_0():
  c = {}
  pc = 0
  c['passive checks'] = {}
  c['passive checks'][pc] = {}
  c['passive checks'][pc]['command'] = 'echo foo'
  test = check.run_check(c, pc, False)
  assert test['code'] == 0
  assert test['stdout'] == "foo"
  assert test['stderr'] == ""

def test_run_check_check_load_OK():
  cmd = '/usr/local/libexec/nagios/check_load'
  if os.path.isfile(cmd):
    c = {}
    pc = 0
    c['passive checks'] = {}
    c['passive checks'][pc] = {}
    c['passive checks'][pc]['command'] = cmd + ' -w 100,100,100 -c 200,200,200'
    test = check.run_check(c, pc, False)
    assert test['code'] == 0
    assert "OK - load average: " in test['stdout']
    assert test['stderr'] == ""

def test_run_check_check_load_warn():
  cmd = '/usr/local/libexec/nagios/check_load'
  if os.path.isfile(cmd):
    c = {}
    pc = 0
    c['passive checks'] = {}
    c['passive checks'][pc] = {}
    c['passive checks'][pc]['command'] = cmd + ' -w 0,0,0 -c 200,200,200'
    test = check.run_check(c, pc, False)
    assert test['code'] == 1
    assert "WARNING - load average: " in test['stdout']
    assert test['stderr'] == ""

def test_run_check_check_load_crit():
  cmd = '/usr/local/libexec/nagios/check_load'
  if os.path.isfile(cmd):
    c = {}
    pc = 0
    c['passive checks'] = {}
    c['passive checks'][pc] = {}
    c['passive checks'][pc]['command'] = cmd + ' -w 0,0,0 -c 0,0,0'
    test = check.run_check(c, pc, False)
    assert test['code'] == 2
    assert "CRITICAL - load average: " in test['stdout']
    assert test['stderr'] == ""
