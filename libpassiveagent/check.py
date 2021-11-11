import configparser
import json
import logging
import os
import requests
import sys
import subprocess

from libpassiveagent import schedule

def check_check(config):
  dir = config['plugin directives']['plugin_path']
  if os.path.isdir(dir):
    for f in config['passive checks']:
      file = os.path.join(dir,config['passive checks'][f].split()[0])
      if not os.path.isfile(file):
        logging.warning('%s: is not accessible', file)
        config.remove_option('passive checks', f)
  else: # isdir
    logging.error('plugin_path: %s: is not accessible', dir)
    sys.exit(2)

  return config

def run_check(c, pc, reschedule_and_post=True):
  if reschedule_and_post:
    schedule.reschedule(c, pc)
  logging.info('run_check(): %s', c['passive checks'][pc]['command'].split())
  if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
    res = subprocess.run(c['passive checks'][pc]['command'].split(), capture_output=True, text=True)
  else:
    res = subprocess.run(c['passive checks'][pc]['command'].split(), stdout=subprocess.PIPE, universal_newlines=True)
  logging.info('run_check(): returncode: %s; stdout: %s', res.returncode, res.stdout.rstrip())
  if reschedule_and_post:
    post_results(c, pc, { "code": res.returncode, "stdout": res.stdout.rstrip() })
  else:
    return { "code": res.returncode, "stdout": res.stdout.rstrip(), "stderr": res.stderr.rstrip() }

def post_results(c, pc, res):
  data = {}
  data['checkresults'] = []
  data['checkresults'].append({})
  data['checkresults'][0]['hostname'] = c['passive checks'][pc]['hostname']
  data['checkresults'][0]['servicename'] = c['passive checks'][pc]['checkname']
  data['checkresults'][0]['state'] = res['code']
  data['checkresults'][0]['output'] = res['stdout']
  data['checkresults'][0]['checkresult'] = {}
  data['checkresults'][0]['checkresult']['type'] = "service"
  postdata = {}
  postdata['host']  = c['passive checks'][pc]['hostname']
  postdata['debug'] = 1
  postdata['type']  = "service"
  postdata['cmd']   = "submitcheck"
  postdata['token'] = c['nrdp']['token']
  postdata['json']  = json.dumps(data)
  for u in c['nrdp']['parent']:
    if not u.endswith('/'):
      u += '/'
    try:
      r = requests.post(u, data=postdata, timeout=10)
    except requests.Timeout:
      logging.warning('Timeout posting results to %s', u)
    else:
      if r.status_code == requests.codes.ok:
        logging.info('Submitted successfully to NRDP: %s', u)
      else:
        logging.warning('Failed submitting to NRDP: %s; Error: %s: ', u, r.status_code)
