import configparser
import logging
import os
import socket
import sys

from passiveagent import check

def check_command(cmd):
  # escape hatch for space seperated arguments
  if " " in cmd:
    if os.path.isfile(cmd.split()[0]):
      return cmd
  if not os.path.isfile(cmd):
    command = cmd.split('/')
    command.remove('')
    i = 0
    l = len(command)
    while i < l:
      # assemble the array minus i
      tempcmd = ""
      for x in range(l - i):
        tempcmd += '/' + command[x]
        if os.path.isfile(tempcmd):
          # Add args to the end
          for j in range(i + 1, l):
            tempcmd += ' ' + command[j]
          return tempcmd
        else:
          i += 1
  else:
    return cmd

def read_config(c):
  config = configparser.ConfigParser()
  parsed = {}
  success = False
  for root, dirs, files in os.walk(c['config_dir']):
    for name in files:
      if name.endswith('.cfg'):
        f = os.path.join(root,name)
        try:
          config.read(f)
          success = True
        except Exception as e:
          logging.error('Error opening and reading: %s', str(e))
          print(f'Error opening and reading: {f}: {str(e)}')
          sys.exit(2)
  if success:
    if 'nrdp' in config:
      c['nrdp'] = {}
      for k in config['nrdp']:
        if k == 'parent':
          if "," in config['nrdp'][k]:
            c['nrdp'][k] = []
            for item in config['nrdp'][k].split(','):
              c['nrdp'][k].append(item.lstrip())
          else:
            c['nrdp'][k] = [ config['nrdp'][k] ]
        else:
          c['nrdp'][k] = config['nrdp'][k]
    if 'passive checks' in config:
      c['passive checks'] = {}
      for k in config['passive checks']:
        c['passive checks'][k] = {}
        s = k.split('|')
        # hostname
        if s[0] != '%hostname%':
          c['passive checks'][k]['hostname'] = s[0]
        else:
          if 'hostname' in c['nrdp']:
            c['passive checks'][k]['hostname'] = c['nrdp']['hostname']
          else:
            c['passive checks'][k]['hostname'] = socket.gethostname()
        # checkname/interval
        if len(s) == 2:
          c['passive checks'][k]['checkname'] = s[1]
          c['passive checks'][k]['interval'] = 300
        if len(s) > 2:
          c['passive checks'][k]['checkname'] = s[1]
          if int(s[2]) > 10 and int(s[2]) < 86400:
            c['passive checks'][k]['interval'] = int(s[2])
          else:
            logging.warning(
              'interval for %s, outside of min(10)/max(86400): %s defaulting to 300s',
              s[1], int(s[2]))
            c['passive checks'][k]['interval'] = 300
        # command
        if config['passive checks'][k].startswith('/'):
          c['passive checks'][k]['command'] = config['passive checks'][k]
        else:
          if config['plugin directives']['plugin_path'].endswith('/'):
            c['passive checks'][k]['command'] = config['plugin directives']['plugin_path'] + config['passive checks'][k]
          else:
            c['passive checks'][k]['command'] = config['plugin directives']['plugin_path'] + '/' + config['passive checks'][k]
        # strip slash components away
        # %HOSTNAME%|dns|60 = check_dns/-H/_healthcheck.corp.care2.com/-q/TXT/-t/5:3
        print(f'passive command: {c["passive checks"][k]["command"]}')
        c['passive checks'][k]['command'] = check_command(c['passive checks'][k]['command'])
        if c['passive checks'][k]['command'] == None:
          logging.warning('unable to find command for: %s', c['passive checks'][k]['checkname'])
          c['passive checks'].pop(k)
  else:
    print(f'No .cfg files found in {c["config_dir"]}')
    logging.error('No .cfg files found in: %s', c['config_dir'])
    sys.exit(2)
