import os
import time
import socket

from ncbi.lbos import Lbos, LbosDomain


def register_loop():
    registered = False
    while True:
        if not registered:
            try:
                domain = getattr(LbosDomain, os.environ['LBOS_DOMAIN'])
            except KeyError:
                domain = None
            except AttributeError:
                raise Exception((
                    "LBOS_DOMAIN variable has incorrect value. "
                    "The choices are {}.".format(LbosDomain.available_domains())
                ))

            print("registering for domain {} from process {}".format(domain, os.getpid()))
            client = Lbos(domain=domain)

            ip = socket.gethostbyname(socket.gethostname())
            try:
                port = os.environ['PORT']
            except KeyError:
                port = '8080'

            try:
                check_url = os.environ['CHECK_URL']
            except KeyError:
                check_url = '/'

            try:
                version = os.environ['VERSION']
                app_name = os.environ['APP_NAME']
            except KeyError:
                raise Exception("APP_NAME and VERSION are required environment variables.")

            registered = client.announce(app_name, version, ip, port=port, check_url=check_url)
            if registered:
                print("Congratulations! Your announcement for {}:{} was successful!".format(ip, port))
            else:
                print("Announcement for: {},{},{},{},{} failed.".format(app_name, version, ip, port, check_url))
        time.sleep(900)


if __name__ == '__main__':
    register_loop()
