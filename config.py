import configparser
import os

def read_config(configdir):
  config = configparser.ConfigParser()
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
    return config
  else:
    print(f'No .cfg files found in {configdir}')
    sys.exit(2)
