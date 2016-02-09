import os
import time
import requests

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=2, pool_maxsize=4, pool_connections=1)
session.mount('https://www.ncbi.nln.nih.gov', adapter)


def register_loop():
    while True:
        print("registering {} from process {}".format(os.getenv("LBOSADDRESS"), os.getpid()))
        # wait for 15m to re-register
        time.sleep(900)


if __name__ == '__main__':
    register_loop()
