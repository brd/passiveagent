import sched

def clear_sched(s):
  for i in s.queue:
    s.cancel(i)

def start_sched(config):
  s = sched.scheduler()
  for c in config['passive checks']:
    s.enter(config['passive checks'][c]['interval'] - 7,
      run_test(config['passive checks'][c]['command'])

  s.run
  return s
