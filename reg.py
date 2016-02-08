import os
import time
import requests
import fcntl
from uwsgidecorators import *

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=2, pool_maxsize=4, pool_connections=1)
session.mount('https://www.ncbi.nln.nih.gov', adapter)

@postfork
def pf():
    f = open('lock.tmp', 'w+')
    print(os.getenv("B"))
    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("Got the lock on pid: {}".format(os.getpid()))
        for x in xrange(0,4):
            print("Doing work, time {}, on pid: {}".format(x, os.getpid()))
            print(session.get('https://www.ncbi.nlm.nih.gov/').status_code)
            # really? boo
            time.sleep(1.5)
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
