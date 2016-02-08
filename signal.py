import uwsgi
import os
from uwsgidecorators import *

@postfork
def register_signal():
    print("Signal mule1 from pid:{}".format(os.getpid()))
    uwsgi.mule_msg('announce', 1)
