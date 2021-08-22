import configparser
import logging
import os
import sys
import subprocess

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

def run_check(cmd):
  logging.info(f'run_check(): {cmd.split()}')
  res = subprocess.run(cmd.split(), capture_output=True, text=True)
  logging.info(f'run_check(): returncode: {res.returncode}; stdout: {res.stdout.rstrip()}')
  return { "code": res.returncode, "stdout": res.stdout.rstrip(), "stderr": res.stderr.rstrip() }
