#!/usr/bin/env python

import argparse
import logging
import os
import requests
import signal
import sys

from libpassiveagent import check
from libpassiveagent import config
from libpassiveagent import schedule

global c
c = {}

def initialize_signal_handlers():
  signal.signal(signal.SIGHUP, handle_sighup)
  signal.signal(signal.SIGINT, handle_exit)
  signal.signal(signal.SIGTERM, handle_exit)

def handle_sighup(signal, frame):
  logging.warning('SIGHUP recieved, reloading config..')
  schedule.clear_sched(c)
  config.read_config(c)
  schedule.start_sched(c)

def handle_exit(signum, frame):
  if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    logging.warning('%s recieved, exiting..', signal.strsignal(signum))
  else:
    logging.warning('exiting..')
  remove_pid(c['pidfile'])
  sys.exit(0)

def remove_pid(pidfile):
  if os.path.isfile(pidfile):
    os.remove(pidfile)

def daemonize():
  try:
    pid = os.fork()
    if pid > 0:
      sys.exit(0)
  except OSError as err:
    sys.stderr.write('Fork #1 failed: {0}\n'.format(err))
    sys.exit(1)

  # detach from parent environment
  os.chdir('/')
  os.setsid()
  os.umask(0)
  # second fork
  try:
    pid = os.fork()
    if pid > 0:
      # exit from second parent
      sys.exit(0)
  except OSError as err:
    sys.stderr.write('Fork #2 failed: {0}\n'.format(err))
    sys.exit(1)
  # redirect std file descriptors
  sys.stdout.flush()
  sys.stderr.flush()
  stdin  = open(os.devnull, 'r')
  stdout = open(os.devnull, 'w')
  stderr = open(os.devnull, 'w')
  os.dup2(stdin.fileno(), sys.stdin.fileno())
  os.dup2(stdout.fileno(), sys.stdout.fileno())
  os.dup2(stderr.fileno(), sys.stderr.fileno())

def main():
  parser = argparse.ArgumentParser(description="Passive Agent")
  parser.add_argument('-c', '--configdir',
    default='/usr/local/etc/passiveagent',
    help='override the location of the configdir')
  parser.add_argument('-f', '--foreground', action='store_true',
    help='Do not detach and become a deamon')
  parser.add_argument('-l', '--logfile',
    default='/var/log/passiveagent.log',
    help='override the location of the logfile')
  parser.add_argument('-p', '--pidfile',
    default='/var/run/passiveagent.pid',
    help='override the location of the pidfile')
  args = parser.parse_args()
  c['config_dir'] = args.configdir

  # Detach from the controlling terminal
  if not args.foreground:
    daemonize()

  # Setup logging
  logging.basicConfig(filename=args.logfile, level=logging.INFO,
    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S')
  logging.info('Starting up..')

  # Setup pidfile
  c['pidfile'] = args.pidfile
  try:
    with open(c['pidfile'], "w") as p:
      p.write(str(os.getpid()))
  except Exception as e:
    logging.error('Unable to create pidfile: %s: %s', c['pidfile'], e)
    sys.exit(2)

  initialize_signal_handlers()

  config.read_config(c)
  schedule.start_sched(c)

if __name__ == '__main__':
  main()
