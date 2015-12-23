import time
import uwsgi
import requests

s = requests.Session()

def register(signum):
    start_time = time.time()
    print("**********************here is the signum: {}".format(signum))
    s.get("http://www.ncbi.nlm.nih.gov")
    print("--- %s seconds ---" % (time.time() - start_time))

uwsgi.register_signal(99, "", register)
uwsgi.add_timer(99, 3)
