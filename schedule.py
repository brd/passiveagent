import sched

import check

def clear_sched(c):
  for i in c['s'].queue:
    c['s'].cancel(i)

def start_sched(c):
  c['s'] = sched.scheduler()
  for pc in c['passive checks']:
    print(f'scheduling: {pc} in {c["passive checks"][pc]["interval"] - 7}')
    c['s'].enter(c['passive checks'][pc]['interval'] - 7, 1,
      check.run_check, argument=(c, pc,))

  c['s'].run()

def reschedule(c, pc):
  c['s'].enter(c['passive checks'][pc]['interval'] - 7, 1,
    check.run_check, argument=(c, pc,))
