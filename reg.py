import os
import time
import uwsgi
import requests
import fcntl
from uwsgidecorators import *

# s = requests.Session()

# def register(signum):
#     start_time = time.time()
#     print("**********************here is the signum: {}".format(signum))
#     s.get("http://www.ncbi.nlm.nih.gov")
#     print("--- %s seconds ---" % (time.time() - start_time))

# uwsgi.register_signal(99, "", register)
# uwsgi.add_timer(99, 3)


# @postfork
# def pf():
#     """This returns 1 each time, b/c each post-fork is in a different thread/process"""
#     global x
#     x = x + 1
#     print("Post-fork hook called, time number {}".format(x))


@postfork
def pf():
    f = open('lock.tmp', 'w+')
    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("Got the lock on pid: {}".format(os.getpid()))
        for x in xrange(0,10):
            print("Doing work, time {}, on pid: {}".format(x, os.getpid()))
            time.sleep(1)
    except IOError, e:
        print("Unable to retrieve lock for fileno {}, pid: {}".format(f.fileno(), os.getpid()))
    finally:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            print("Releasing the lock from pid: {}".format(os.getpid()))
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            f.close()
        except IOError, e:
            print("Finally on process that can't get lock, pid: {}".format(os.getpid()))
