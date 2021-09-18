import configparser
import logging
import os
import requests
import sys
import subprocess

import schedule

def check_check(config):
  dir = config['plugin directives']['plugin_path']
  if os.path.isdir(dir):
    for f in config['passive checks']:
      print(f'f: {f}')
      print(f'line: {config["passive checks"][f]}')
      file = os.path.join(dir,config['passive checks'][f].split()[0])
      if not os.path.isfile(file):
        logging.warning('%s: is not accessible', file)
        print(f'check: {file} is not accessible')
        config.remove_option('passive checks', f)
  else: # isdir
    logging.error('plugin_path: %s: is not accessible', dir)
    print(f'plugin_path: {dir} is not accessible')
    sys.exit(2)

  return config

def run_check(c, pc, reschedule_and_post=True):
  if reschedule_and_post:
    schedule.reschedule(c, pc)
  logging.info('run_check(): %s', c['passive checks'][pc]['command'].split())
  res = subprocess.run(c['passive checks'][pc]['command'].split(), capture_output=True, text=True)
  logging.info('run_check(): returncode: %s; stdout: %s', res.returncode, res.stdout.rstrip())
  if reschedule_and_post:
    post_results(c, pc, { "code": res.returncode, "stdout": res.stdout.rstrip() })
  else:
    return { "code": res.returncode, "stdout": res.stdout.rstrip(), "stderr": res.stderr.rstrip() }

def post_results(c, pc, res):
  data = {}
  data['checkresults'] = []
  data['checkresults'].append({})
  data['checkresults'][0]['service'] = {}
  data['checkresults'][0]['service']['hostname'] = c['passive checks'][pc]['hostname']
  data['checkresults'][0]['service']['servicename'] = c['passive checks'][pc]['checkname']
  data['checkresults'][0]['service']['state'] = res['code']
  data['checkresults'][0]['service']['output'] = res['stdout']
  print(data)
  for u in c['nrdp']['parent']:
    if not u.endswith('/'):
      u += '/'
    r = requests.post(u, json=data, timeout=10)
    if r.status_code == requests.codes.ok:
      logging.info('Submitted successfully to NRDP: %s', u)
    else:
      logging.warning('Failed submitting to NRDP: %s; Error: %s: ', u, r.status_code)
