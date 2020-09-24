from datetime import datetime
import json
from models.task import Task
import pytz
from utils.DBDriver import DBDriver


class KanbanBoardService:
    COST_PER_HOUR = 1000

    def __init__(self):
        self.dbms = DBDriver()

    def create_task(self, event):
        body = dict()
        is_valid = True
        result = {
            'data': {},
            'status': 201  # Created.
        }
        if event['body'] is None:
            result['data'] = {'error': 'body is not set'}
            result['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid:
            body = json.loads(event['body'])
            if not bool(body):
                result['data'] = {'error': 'body is empty'}
                result['status'] = 400  # Bad Request.
                is_valid = False
        if is_valid:
            if 'title' not in body:
                result['data'] = {'error': 'title is not set'}
                result['status'] = 400  # Bad Request.
                is_valid = False
            else:
                body['title'] = body['title'].strip()
        if is_valid and not body['title']:
            result['data'] = {'error': 'title is empty'}
            result['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid:
            task = Task(title=body['title'])
            session = self.dbms.get_session()
            try:
                session.add(task)
                session.commit()
                result['data'] = self.map_to_json(task)
            except Exception as ex:
                session.rollback()
                print(ex)
            finally:
                session.close()
        return result

    def get_tasks(self, event):
        result = {
            'data': {},
            'status': 200  # OK.
        }
        session = self.dbms.get_session()
        try:
            tasks = session.query(Task).all()
            objects = []
            if tasks:
                for task in tasks:
                    obj = self.map_to_json(task)
                    objects.append(obj)
            result['data'] = objects
        except Exception as ex:
            print(ex)
        finally:
            session.close()
        return result

    def update_task(self, event):
        body = dict()
        is_valid = True
        result = {
            'data': {},
            'status': 205  # Reset Content.
        }
        id = event['pathParameters']['id']
        if id.isdigit():
            id = int(id)
        else:
            result['data'] = {'error': 'incorrect path'}
            result['status'] = 404  # Not Found.
            is_valid = False
        if is_valid and 'body' not in event:
            result['data'] = {'error': 'no body'}
            result['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid and event['body'] is None:
            result['data'] = {'error': 'body is not set'}
            result['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid:
            body = json.loads(event['body'])
            if not bool(body):
                result['data'] = {'error': 'body is empty'}
                result['status'] = 400  # Bad Request.
                is_valid = False
        if is_valid:
            if 'status' not in body:
                result['data'] = {'error': 'status is not set'}
                result['status'] = 400  # Bad Request.
                is_valid = False
        if is_valid and '' == body['status']:
            result['data'] = {'error': 'status is empty'}
            result['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid:
            update = [
                Task.Statuses.TODO.value,
                Task.Statuses.IN_PROGRESS.value,
                Task.Statuses.DONE.value
            ]
            if body['status'] not in update:
                result['data'] = {'error': 'status is unknown'}
                result['status'] = 400  # Bad Request.
                is_valid = False
        if is_valid:
            session = self.dbms.get_session()
            try:
                task = session.query(Task).get(id)
                if body['status'] == task.status:
                    result['data'] = {'error': 'status is not changed'}
                    result['status'] = 400  # Bad Request.
                    is_valid = False
                elif body['status'] - 1 != task.status:
                    result['data'] = {'error': 'status is incorrect'}
                    result['status'] = 409  # Conflict.
                    is_valid = False
                if is_valid:
                    task.status = body['status']
                    if task.status == task.Statuses.IN_PROGRESS.value:
                        task.start_time = datetime.now(tz=pytz.UTC)
                    elif task.status == task.Statuses.DONE.value:
                        task.end_time = datetime.now(tz=pytz.UTC)
                        delta = task.end_time - task.start_time
                        hours = delta.total_seconds() / 3600
                        task.payment = hours * KanbanBoardService.COST_PER_HOUR
                        task.payment = round(task.payment, 2)
                    session.add(task)
                    session.commit()
                    result['data'] = self.map_to_json(task)
            except Exception as ex:
                session.rollback()
                print(ex)
            finally:
                session.close()
        return result

    def map_to_json(self, task):
        obj = {
            "id": task.id,
            "title": task.title,
            "start_time": None,
            "end_time": None,
            "status": task.status,
            "payment": task.payment
        }
        if task.start_time:
            obj['start_time'] = task.start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
        if task.end_time:
            obj['end_time'] = task.end_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return obj
