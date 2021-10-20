import logging
import random
import sched

from passiveagent import check

def clear_sched(c):
  for i in c['s'].queue:
    c['s'].cancel(i)

def start_sched(c):
  c['s'] = sched.scheduler()
  for pc in c['passive checks']:
    r = random.randrange(1,20)
    logging.warning(f'scheduling initial check: {pc} in {r}')
    c['s'].enter(r, 1, check.run_check, argument=(c, pc,))

  c['s'].run()

def reschedule(c, pc):
  r = random.randrange(1,7)
  c['s'].enter(c['passive checks'][pc]['interval'] - r, 1,
    check.run_check, argument=(c, pc,))
