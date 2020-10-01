import unittest
from unittest.mock import patch

from utils.DBDriver import DBDriver

mock_data = {
    'user': 'test-user',
    'pass': 'test-pass',
    'host': '0.0.0.0',
    'port': '1111',
    'dbname': 'test-db-name'
}


class TestDBDriver(unittest.TestCase):
    """Test DBDriver."""

    @patch('os.environ', mock_data)
    def test_create_engine(self):
        """Test: _create_engine(self)"""

        driver = DBDriver()
        db = driver.get_dbms()
        self.assertRegex(db.__str__(), mock_data['user'])
        self.assertRegex(db.__str__(), mock_data['host'])
        self.assertRegex(db.__str__(), mock_data['port'])
        self.assertRegex(db.__str__(), mock_data['dbname'])
