#!/usr/bin/env python

import argparse
import logging
import requests
import signal
import sys

from passiveagent import check
from passiveagent import config
from passiveagent import schedule

global c
c = {}
c['config_dir'] = '/usr/local/passive-agent/etc'

def initialize_signal_handlers():
  signal.signal(signal.SIGHUP, handle_sighup)
  signal.signal(signal.SIGINT, handle_exit)
  signal.signal(signal.SIGTERM, handle_exit)

def handle_sighup(signal, frame):
  logging.warning('SIGHUP recieved, reloading config..')
  clear_sched(c)
  read_config(c)
  schedule.start_sched(c)

def handle_exit(signum, frame):
  logging.warning('%s recieved, exiting..', signal.strsignal(signum))
  sys.exit(0)

def main():
  parser = argparse.ArgumentParser(description="Passive Agent")
  parser.add_argument('-l', '--logfile', default='/var/log/lite.log',
    help='override the location of the logfile')
  args = parser.parse_args()
  print(f'args: {args.log}')
  sys.exit(3)
  # Setup logging
  logging.basicConfig(filename=args.logfile, level=logging.INFO,
    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S')
  logging.info('Starting up..')
  initialize_signal_handlers()

  config.read_config(c)
  schedule.start_sched(c)

if __name__ == '__main__':
  main()
