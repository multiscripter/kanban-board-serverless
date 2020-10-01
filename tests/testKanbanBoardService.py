import pytz
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

from models.task import Task
from services.kanbanBoardService import KanbanBoardService


class TestKanbanBoardService(unittest.TestCase):
    """Test KanbanBoardService."""

    def setUp(self):
        self.service = KanbanBoardService()

        with patch('sqlalchemy.orm.query.Query') as MockQuery:
            self.mock_query = MockQuery.return_value
            self.mock_query.all.return_value = [
                Task(**{
                    'id': 1,
                    'title': 'mock-title-1',
                    'start_time': None,
                    'end_time': None,
                    'status': 0,
                    'payment': 0
                }),
                Task(**{
                    'id': 2,
                    'title': 'mock-title-2',
                    'start_time': None,
                    'end_time': None,
                    'status': 0,
                    'payment': 0
                })
            ]

        with patch('sqlalchemy.orm.session.Session') as MockSession:
            self.mock_session = MockSession.return_value
            self.mock_session.add.return_value = None
            self.mock_session.commit.return_value = None
            self.mock_session.close.return_value = None
            self.mock_session.query.return_value = self.mock_query

        with patch('utils.DBDriver.DBDriver') as MockDBDriver:
            self.service.dbms = MockDBDriver.return_value
            self.service.dbms.get_session.return_value = self.mock_session

    def test_create_task_success(self):
        """Test: create_task(self, event)"""

        title = 'some-title'
        event = {
            'body': f'{{"title": "{title}"}}'
        }

        actual = self.service.create_task(event)

        self.assertEqual(201, actual['status'])
        self.assertEqual(title, actual['data']['title'])

    def test_create_task_exception(self):
        """Test: create_task(self, event)
        session.commit() throws Exception"""

        self.mock_session.commit.side_effect = Mock(side_effect=Exception())
        title = 'some-title'
        event = {
            'body': f'{{"title": "{title}"}}'
        }

        actual = self.service.create_task(event)
        self.assertEqual(500, actual['status'])
        self.assertEqual(
            'session.commit error', actual['data']['errors']['db']
        )

    def test_create_task_errors(self):
        """Test: create_task(self, event)
        returns errors."""

        event = {
            'body': '{"title": ""}'
        }
        actual = self.service.create_task(event)

        self.assertEqual(400, actual['status'])
        self.assertEqual(
            'title is empty', actual['data']['errors']['title']
        )

    def test_get_tasks_success(self):
        """Test: get_tasks(self, event)"""

        actual = self.service.get_tasks(None)
        self.assertEqual(200, actual['status'])
        self.assertEqual(2, len(actual['data']))

    def test_get_tasks_exception(self):
        """Test: create_task(self, event)
        session.query(Task).all() throws Exception"""

        self.mock_query.all.side_effect = Mock(side_effect=Exception())

        actual = self.service.get_tasks(None)
        self.assertEqual(500, actual['status'])
        self.assertEqual(
            'session.query.all error', actual['data']['errors']['db']
        )

    def test_update_task_success_status_in_progress(self):
        """Test: update_task(self, event).
        Status: IN_PROGRESS."""

        self.mock_query.get.return_value = Task(**{
            'id': 3,
            'title': 'mock-title-3',
            'start_time': None,
            'end_time': None,
            'status': 0,
            'payment': 0
        })
        status = Task.Statuses.IN_PROGRESS.value
        event = {
            'body': f'{{"status": {status}}}',
            'pathParameters': {
                'id': '3'
            }
        }
        actual = self.service.update_task(event)
        self.assertEqual(205, actual['status'])
        self.assertEqual(status, actual['data']['status'])

    def test_update_task_success_status_done(self):
        """Test: update_task(self, event).
        Status: DONE."""

        start_dt = datetime.now(tz=pytz.UTC)
        start_dt = start_dt - timedelta(days=1)
        start_dt = start_dt.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        self.mock_query.get.return_value = Task(**{
            'id': 3,
            'title': 'mock-title-3',
            'start_time': start_dt,
            'end_time': None,
            'status': Task.Statuses.IN_PROGRESS.value,
            'payment': 0
        })
        status = Task.Statuses.DONE.value
        event = {
            'body': f'{{"status": {status}}}',
            'pathParameters': {
                'id': '3'
            }
        }
        actual = self.service.update_task(event)
        self.assertEqual(205, actual['status'])
        self.assertEqual(status, actual['data']['status'])

    def test_update_task_id_incorrect_path(self):
        """Test: update_task(self, event).
        Error: incorrect path."""

        event = {
            'pathParameters': {
                'id': 'fake'
            }
        }
        actual = self.service.update_task(event)
        self.assertEqual(404, actual['status'])
        self.assertEqual(
            'incorrect path', actual['data']['errors']['common']
        )

    def test_update_task_error_status_is_unknown(self):
        """Test: update_task(self, event).
        Error: status is unknown."""

        event = {
            'body': '{"status": "fake-status"}',
            'pathParameters': {
                'id': '3'
            }
        }
        actual = self.service.update_task(event)
        self.assertEqual(400, actual['status'])
        self.assertEqual(
            'status is unknown', actual['data']['errors']['status']
        )

    def test_update_task_error_status_is_not_changed(self):
        """Test: update_task(self, event).
        Error: status is not changed."""

        status = Task.Statuses.TODO.value
        self.mock_query.get.return_value = Task(**{
            'id': 3,
            'title': 'mock-title-3',
            'start_time': None,
            'end_time': None,
            'status': status,
            'payment': 0
        })
        event = {
            'body': f'{{"status": {status}}}',
            'pathParameters': {
                'id': '3'
            }
        }
        actual = self.service.update_task(event)
        self.assertEqual(400, actual['status'])
        self.assertEqual(
            'status is not changed', actual['data']['errors']['status']
        )

    def test_update_task_error_status_is_incorrect(self):
        """Test: update_task(self, event).
        Error: status is incorrect."""

        status = Task.Statuses.IN_PROGRESS.value
        self.mock_query.get.return_value = Task(**{
            'id': 3,
            'title': 'mock-title-3',
            'start_time': None,
            'end_time': None,
            'status': status,
            'payment': 0
        })
        status = Task.Statuses.TODO.value
        event = {
            'body': f'{{"status": {status}}}',
            'pathParameters': {
                'id': '3'
            }
        }
        actual = self.service.update_task(event)
        self.assertEqual(409, actual['status'])
        self.assertEqual(
            'status is incorrect', actual['data']['errors']['status']
        )

    def test_update_task_exception(self):
        """Test: update_task(self, event)
        session.query(Task).all() throws Exception"""

        self.mock_query.get.return_value = Task(**{
            'id': 3,
            'title': 'mock-title-3',
            'start_time': None,
            'end_time': None,
            'status': 0,
            'payment': 0
        })
        status = Task.Statuses.IN_PROGRESS.value
        event = {
            'body': f'{{"status": {status}}}',
            'pathParameters': {
                'id': '3'
            }
        }
        self.mock_session.commit.side_effect = Mock(side_effect=Exception())
        actual = self.service.update_task(event)
        self.assertEqual(500, actual['status'])
        self.assertEqual(
            'session.commit error', actual['data']['errors']['db']
        )
