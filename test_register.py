import signal
import sys
from register import register_loop
from unittest import TestCase


PY3 = sys.version_info[0] == 3
if PY3:
    from unittest.mock import patch
else:
    from mock import patch


class TimeoutError(Exception):
    pass


def signal_handler(signum, frame):
    raise TimeoutError("Timed out!")


class TestRegister(TestCase):

    def test_required_environment_variables(self):
        with self.assertRaises(ValueError):
            register_loop()

    def test_app_name_required(self):
        with patch.dict('os.environ', {
            'VERSION': '1.3.0'
        }):
            with self.assertRaises(ValueError):
                register_loop()

    def test_version_required(self):
        with patch.dict('os.environ', {
            'APP_NAME': 'my-app'
        }):
            with self.assertRaises(ValueError):
                register_loop()

    def test_no_exceptions(self):
        """
        This test uses signals to terminate an infinite loop.
        'signal.alarm(3)' sends signal.SIGALRM after 3 seconds
        which causes TimeoutError and ends loop.
        """
        with patch.dict('os.environ', {
            'APP_NAME': 'my-app',
            'VERSION': '1.3.0'
        }):
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(3)   # 3 seconds
            try:
                register_loop()
            except TimeoutError:
                pass


if __name__ == '__main__':
    unittest.main()

