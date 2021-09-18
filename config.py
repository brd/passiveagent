import configparser
import os
import socket

import check

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
        if s[0] != '%%hostname%%':
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
  else:
    print(f'No .cfg files found in {c["config_dir"]}')
    logging.error('No .cfg files found in: %s', c['config_dir'])
    sys.exit(2)
