import json
import unittest
from io import BytesIO
import pycurl


class TestService (unittest.TestCase):
    """Test kanbanBoardController."""

    def test_error_route_not_found(self):
        """Test: Method GET, URI dev/tasks/100500
        Get tasks. Error: 404. Incorrect path."""

        actual = request('/fake-route')
        self.assertTrue(404, actual['statusCode'])
        self.assertTrue('route not found' in actual['error'])

    def test_get_site_root(self):
        """Test: Method GET, URI dev/
        Request site root."""

        actual = request()
        # self.assertTrue(200, actual['status'])
        self.assertEqual('Kanban-board!', actual['message'])

    def test_get_tasks(self):
        """Test: Method GET, URI dev/tasks
        Get all tasks."""

        actual = request('/tasks')
        self.assertEqual(1, len(actual))


def request(uri='', method='GET', data=None):
    bytes_obj = BytesIO()
    _curl = pycurl.Curl()
    _curl.setopt(_curl.URL, 'http://localhost:3000/dev' + uri)
    _curl.setopt(_curl.WRITEDATA, bytes_obj)
    _curl.perform()
    _curl.close()

    bytes_str = bytes_obj.getvalue()
    decoded = bytes_str.decode('utf8')
    response = json.loads(decoded)
    return response
