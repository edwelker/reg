import os
import time
import socket
from decouple import config, UndefinedValueError
import logging
from ncbi.lbos import Lbos


# uwsgi package can be imported only when uwsgi instance started
try: # for tests
    import uwsgi
except:
    pass


try:
    # use log file if it was specified
    logfile = uwsgi.opt['logto']
    logging.basicConfig(file=logfile, level=logging.INFO)
except KeyError:
    logging.basicConfig(handler=logging.StreamHandler, level=logging.INFO)
except NameError: # for tests
    pass


logger = logging.getLogger()


def register_loop():
    registered = False
    pid = os.getpid()
    ip = socket.gethostbyname(socket.gethostname())
    port = config('PORT', default='8080')

    check_url = config('CHECK_URL', default='/')

    try:
        version = config('VERSION')
        app_name = config('APP_NAME')
    except UndefinedValueError:
        msg = "VERSION and APP_NAME are required environment variables."
        logger.exception(msg)
        raise ValueError(msg)

    while True:
        if not registered:
            client = Lbos()
            logger.info("Registering to {} from process {}".format(client.lbos_url, pid))

            registered = client.announce(app_name, version, ip, port=port, check_url=check_url)
            if registered:
                logger.info("Congratulations! Your announcement for {}:{} was successful!".format(ip, port))
            else:
                # to be compatible with awesome uwsgi messages
                logger.info("Cry! Announcement for: {},{},{},{},{} failed!!! Let me try again in 15 mins...".format(
                    app_name, version, ip, port, check_url)
                )
        time.sleep(900) # 15 minutes


if __name__ == '__main__':
    register_loop()

