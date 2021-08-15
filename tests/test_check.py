import pytest
import os

import check

def test_check_check():
  config = {}
  config['plugin directives'] = {}
  config['plugin directives']['plugin_path'] = '/usr/local/libexec/nagios'
  config['passive checks'] = {}
  config['passive checks']['%%HOSTNAME%%|ZPOOL'] = 'check_zpools -p ALL'
  check.check_check(config)

def test_run_check_bad_path():
  with pytest.raises(FileNotFoundError) as execinfo:
    check.run_test('/bin/foobar')

def test_run_check_exit_1():
  test = check.run_test('/bin/ls lkjsdlfjasdfljsalkdajfjl')
  assert test['code'] == 1
  assert test['stdout'] == ""
  assert test['stderr'] == "ls: lkjsdlfjasdfljsalkdajfjl: No such file or directory"

def test_run_check_exit_0():
  test = check.run_test('echo foo')
  assert test['code'] == 0
  assert test['stdout'] == "foo"
  assert test['stderr'] == ""

def test_run_check_check_load_OK():
  c = '/usr/local/libexec/nagios/check_load'
  if os.path.isfile(c):
    test = check.run_test(c + ' -w 100,100,100 -c 200,200,200')
    assert test['code'] == 0
    assert "OK - load average: " in test['stdout']
    assert test['stderr'] == ""

def test_run_check_check_load_warn():
  c = '/usr/local/libexec/nagios/check_load'
  if os.path.isfile(c):
    test = check.run_test(c + ' -w 0,0,0 -c 200,200,200')
    assert test['code'] == 1
    assert "WARNING - load average: " in test['stdout']
    assert test['stderr'] == ""

def test_run_check_check_load_crit():
  c = '/usr/local/libexec/nagios/check_load'
  if os.path.isfile(c):
    test = check.run_test(c + ' -w 0,0,0 -c 0,0,0')
    assert test['code'] == 2
    assert "CRITICAL - load average: " in test['stdout']
    assert test['stderr'] == ""
