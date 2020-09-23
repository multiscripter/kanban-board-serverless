from datetime import datetime, timedelta
from models.task import Task
import pytz
import requests
from services.kanbanBoardService import KanbanBoardService
import unittest
from utils.DBDriver import DBDriver


class TestService(unittest.TestCase):
    """Test kanbanBoardController."""

    URL = 'http://localhost:3000/dev'

    @classmethod
    def setUpClass(cls):
        """Actions before all tests."""

        execute_sql_script('../../resources/postgresql-schema.sql')

    def setUp(self):
        """Actions before each test."""

        execute_sql_script('../../resources/postgresql-test-data.sql')

    def test_error_route_not_found(self):
        """Test: Method GET, URI dev/tasks/100500
        Get tasks. Error: 404. Incorrect path."""

        response = requests.get(TestService.URL + '/fake-route')
        actual = response.json()
        self.assertTrue(404, response.status_code)
        self.assertTrue('route not found' in actual['error'])

    def test_get_site_root(self):
        """Test: Method GET, URI dev/
        Request site root."""

        response = requests.get(TestService.URL)
        actual = response.json()
        self.assertEqual('Kanban-board!', actual['message'])

    def test_get_tasks(self):
        """Test: Method GET, URI dev/tasks
        Get all tasks."""

        dbms = DBDriver()
        session = dbms.get_session()
        r_proxy = session.execute('select * from tasks')
        expected = [{col: val for col, val in row.items()} for row in r_proxy]
        session.close()

        response = requests.get(TestService.URL + '/tasks')
        self.assertEqual(200, response.status_code)

        actual = response.json()
        self.assertListEqual(expected, actual)

    def test_create_task(self):
        """Test: Method POST, URI /tasks/
        Create task."""

        data = {
            'title': 'test-task-3'
        }
        response = requests.post(TestService.URL + '/tasks', json=data)
        self.assertEqual(201, response.status_code)

        actual = response.json()
        self.assertTrue(actual['id'] > 0)

    def test_start_task(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Set status = IN_PROGRESS."""

        service = KanbanBoardService()
        data = {
            'status': Task.Statuses.IN_PROGRESS.value
        }
        dbms = DBDriver()
        session = dbms.get_session()
        first = session.query(Task).first()
        first = service.map_to_json(first)
        session.close()
        url = f'{TestService.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json=data)
        self.assertEqual(205, response.status_code)

        actual = response.json()
        self.assertEqual(Task.Statuses.IN_PROGRESS.value, actual['status'])

        expected = datetime.now()
        dt_str = actual['start_time']
        actual = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
        self.assertEqual(expected.date(), actual.date())

    def test_payment_formula(self):
        """Test payment formula."""

        start_dt = datetime.now(tz=pytz.UTC)
        start_dt = start_dt - timedelta(days=1)
        start_dt = start_dt.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        end_dt = start_dt.replace(
            hour=14, minute=15, second=45, microsecond=0
        )
        delta = end_dt - start_dt
        hours = delta.total_seconds() / 3600
        payment = hours * KanbanBoardService.COST_PER_HOUR
        self.assertEqual(262.5, payment)


def execute_sql_script(path=''):
    with open(path) as sql:
        data = sql.read()
        data = data.split(';')
        dbms = DBDriver()
        session = dbms.get_session()
        try:
            for line in data:
                line = line.strip()
                if line:
                    session.execute(line.strip())
            session.commit()
        except Exception as ex:
            session.rollback()
            print(ex)
        finally:
            session.close()
