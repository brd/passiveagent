#!/usr/bin/env python

import config
import logging
import requests
import signal
import sys

import check
import config
import schedule

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
  # Setup logging
  logging.basicConfig(filename='lite.log', level=logging.INFO,
    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S')
  logging.info('Starting up..')
  initialize_signal_handlers()

  config.read_config(c)
  schedule.start_sched(c)

if __name__ == '__main__':
  main()
