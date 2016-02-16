import os
import time
import socket
from decouple import config, UndefinedValueError
import logging
from ncbi.lbos import Lbos


# uwsgi package can be imported only when uwsgi instance started
try: # for tests (hope it's temporarily): http://projects.unbit.it/uwsgi/wiki/TipsAndTricks
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
    while True:
        if not registered:
            client = Lbos()
            logger.info("registering with {} from process {}".format(client.lbos_url, os.getpid()))

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

            registered = client.announce(app_name, version, ip, port=port, check_url=check_url)
            if registered:
                logger.info("Congratulations! Your announcement for {}:{} was successful!".format(ip, port))
            else:
                logger.info("Announcement for: {},{},{},{},{} failed.".format(app_name, version, ip, port, check_url))
        time.sleep(900)


if __name__ == '__main__':
    register_loop()

