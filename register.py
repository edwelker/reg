import os
import time
import requests
import fcntl
from uwsgidecorators import *

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=2, pool_maxsize=4, pool_connections=1)
session.mount('https://www.ncbi.nln.nih.gov', adapter)


def register_loop():
    registered = False
    while registered is not True:
        # message = uwsgi.mule_get_msg()
        print("registering {} from process {}, signal: ".format(os.getenv("LBOSADDRESS"), os.getpid()))
        registered = True
        time.sleep(10)

# uwsgi.register_signal(1, "mule1", register_loop)



if __name__ == '__main__':
    register_loop()
    print("Done with pid: {}".format(os.getpid()))
