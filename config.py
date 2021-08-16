import configparser
import os

def read_config(configdir):
  config = configparser.ConfigParser()
  parsed = {}
  success = False
  for root, dirs, files in os.walk(configdir):
    for name in files:
      if name.endswith('.cfg'):
        f = os.path.join(root,name)
        print(f'file: {f}')
        try:
          config.read(f)
          success = True
        except Exception as e:
          print(f'Error opening and reading: {f}: {str(e)}')
          sys.exit(2)
  if success:
    if 'passive checks' in config:
      parsed['passive checks'] = {}
      for k in config['passive checks']:
        parsed['passive checks'][k] = {}
        s = k.split('|')
        if s[0] != '%%HOSTNAME%%':
          parsed['passive checks'][k]['host'] = s[0]
        if len(s) == 2:
          parsed['passive checks'][k]['checkname'] = s[1]
        if len(s) > 2:
          parsed['passive checks'][k]['checkname'] = s[1]
          parsed['passive checks'][k]['interval'] = s[2]
        parsed['passive checks'][k]['command'] = config['passive checks'][k]
      if 'nrdp' in config:
        parsed['nrdp'] = {}
        for k in config['nrdp']:
          if k == 'parent':
            if "," in config['nrdp'][k]:
              parsed['nrdp'][k] = []
              for item in config['nrdp'][k].split(','):
                parsed['nrdp'][k].append(item.lstrip())
            else:
              parsed['nrdp'][k] = [ config['nrdp'][k] ]
          else:
            parsed['nrdp'][k] = config['nrdp'][k]
    return parsed
  else:
    print(f'No .cfg files found in {configdir}')
    sys.exit(2)
