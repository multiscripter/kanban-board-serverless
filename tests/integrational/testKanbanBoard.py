from datetime import datetime, timedelta
from models.task import Task
import pytz
import requests
from services.kanbanBoardService import KanbanBoardService
import unittest
from utils.DBDriver import DBDriver


class TestKanbanBoard(unittest.TestCase):
    """Test kanbanBoardController."""

    URL = 'http://localhost:3000/dev'

    @classmethod
    def setUpClass(cls):
        """Actions before all tests."""

        execute_sql_script('../../resources/postgresql-schema.sql')

    def setUp(self):
        """Actions before each test."""

        execute_sql_script('../../resources/postgresql-test-data.sql')

    # ---------- Test create task ----------

    def test_create_task_error_body_is_not_set(self):
        """Test: Method POST, URI /tasks/
        Create task. Error: 400. body is not set."""

        response = requests.post(TestKanbanBoard.URL + '/tasks')
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('body is not set', actual['error'])

    def test_create_task_error_body_is_empty(self):
        """Test: Method POST, URI /tasks/
        Create task. Error: 400. body is empty."""

        response = requests.post(TestKanbanBoard.URL + '/tasks', json='{}')
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('body is empty', actual['error'])

    def test_create_task_error_body_title_is_not_set(self):
        """Test: Method POST, URI /tasks/
        Create task. Error: 400. title is not set."""

        data = {
            'foo': 'bar'
        }
        response = requests.post(TestKanbanBoard.URL + '/tasks', json=data)
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('title is not set', actual['error'])

    def test_create_task_error_title_is_empty(self):
        """Test: Method POST, URI /tasks/
        Create task. Error: 400. title is empty."""

        data = {
            'title': ''
        }
        response = requests.post(TestKanbanBoard.URL + '/tasks', json=data)
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('title is empty', actual['error'])

    def test_create_task(self):
        """Test: Method POST, URI /tasks/
        Create task."""

        data = {
            'title': 'test-task-3'
        }
        response = requests.post(TestKanbanBoard.URL + '/tasks', json=data)
        self.assertEqual(201, response.status_code)

        actual = response.json()
        self.assertTrue(actual['id'] > 0)

    # ---------- Test get tasks ----------

    def test_error_route_not_found(self):
        """Test: Method GET, URI dev/tasks/100500
        Get tasks. Error: 404. Incorrect path."""

        response = requests.get(TestKanbanBoard.URL + '/fake-route')
        actual = response.json()
        self.assertTrue(404, response.status_code)
        self.assertTrue('route not found' in actual['error'])

    def test_get_site_root(self):
        """Test: Method GET, URI dev/
        Request site root."""

        response = requests.get(TestKanbanBoard.URL)
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

        response = requests.get(TestKanbanBoard.URL + '/tasks')
        self.assertEqual(200, response.status_code)

        actual = response.json()
        self.assertListEqual(expected, actual)

    # ---------- Test update task ----------

    def test_update_task_error_incorrect_path(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 404. incorrect path."""

        data = {
            'status': 1
        }
        url = f'{TestKanbanBoard.URL}/tasks/fake-path'
        response = requests.patch(url, json=data)
        self.assertEqual(404, response.status_code)

        actual = response.json()
        self.assertEqual('incorrect path', actual['error'])

    def test_update_task_error_body_is_not_set(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 400. body is not set."""

        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url)
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('body is not set', actual['error'])

    def test_update_task_error_body_is_empty(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 400. body is empty."""

        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json={})
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('body is empty', actual['error'])

    def test_update_task_error_status_is_not_set(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 400. status is not set."""

        data = {
            'foo': 'bar'
        }
        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json=data)
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('status is not set', actual['error'])

    def test_update_task_error_status_is_empty(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 400. status is empty."""

        data = {
            'status': ''
        }
        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json=data)
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('status is empty', actual['error'])

    def test_update_task_error_status_is_unknown(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 400. status is unknown."""

        data = {
            'status': 'fake status'
        }
        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json=data)
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('status is unknown', actual['error'])

    def test_update_task_error_status_is_not_changed(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 400. status is not changed."""

        data = {
            'status': Task.Statuses.TODO.value
        }
        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json=data)
        self.assertEqual(400, response.status_code)

        actual = response.json()
        self.assertEqual('status is not changed', actual['error'])

    def test_update_task_error_status_is_incorrect(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Error: 400. status is incorrect."""

        data = {
            'status': Task.Statuses.IN_PROGRESS.value
        }
        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json=data)
        self.assertEqual(205, response.status_code)

        data = {
            'status': Task.Statuses.TODO.value
        }
        response = requests.patch(url, json=data)
        self.assertEqual(409, response.status_code)

        actual = response.json()
        self.assertEqual('status is incorrect', actual['error'])

    def test_update_task_status_in_progress(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Set status = IN_PROGRESS."""

        data = {
            'status': Task.Statuses.IN_PROGRESS.value
        }
        first = get_first()
        url = f'{TestKanbanBoard.URL}/tasks/{first["id"]}'
        response = requests.patch(url, json=data)
        self.assertEqual(205, response.status_code)

        actual = response.json()
        self.assertEqual(Task.Statuses.IN_PROGRESS.value, actual['status'])

        expected = datetime.now()
        dt_str = actual['start_time']
        actual = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
        self.assertEqual(expected.date(), actual.date())

    def test_update_task_status_done(self):
        """Test: Method PATCH, URI /tasks/id
        Update task. Set status = DONE."""

        dbms = DBDriver()
        session = dbms.get_session()
        first = session.query(Task).first()

        url = f'{TestKanbanBoard.URL}/tasks/{first.id}'

        first.status = Task.Statuses.IN_PROGRESS.value
        start_dt = datetime.now(tz=pytz.UTC)
        start_dt = start_dt - timedelta(days=1)
        start_dt = start_dt.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        first.start_time = start_dt
        session.add(first)
        session.commit()
        session.close()

        data = {
            'status': Task.Statuses.DONE.value
        }
        response = requests.patch(url, json=data)
        self.assertEqual(205, response.status_code)

        actual = response.json()
        self.assertEqual(Task.Statuses.DONE.value, actual['status'])

        dt_str = actual['end_time']
        end_dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
        end_dt = pytz.utc.localize(end_dt)
        self.assertTrue(start_dt < end_dt)
        self.assertRegex(str(actual['payment']), '\d+\.\d{,2}')

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


def get_first():
    service = KanbanBoardService()
    dbms = DBDriver()
    session = dbms.get_session()
    first = session.query(Task).first()
    first = service.map_to_json(first)
    session.close()
    return first