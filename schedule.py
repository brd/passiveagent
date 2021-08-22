import sched

import check

def clear_sched(s):
  for i in s.queue:
    s.cancel(i)

def start_sched(config):
  s = sched.scheduler()
  for c in config['passive checks']:
    s.enter(config['passive checks'][c]['interval'] - 7, 1,
      check.run_check(config['passive checks'][c]['command'],
        config['nrdp']['parent']))

  s.run()
  return s
