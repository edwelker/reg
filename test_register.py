import sys
from register import register_loop
from unittest import TestCase


PY3 = sys.version_info[0] == 3
if PY3:
    from unittest.mock import patch
else:
    from mock import patch


class TestRegister(TestCase):

    def test_required_environment_variables(self):
        with patch.dict('os.environ', {'LBOS_URL': 'http://some_another_lbos_url:8080/lbos'}):
            register_loop()


if __name__ == '__main__':
    unittest.main()

