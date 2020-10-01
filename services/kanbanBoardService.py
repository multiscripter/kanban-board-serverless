from datetime import datetime
from models.task import Task
import pytz
from utils.DBDriver import DBDriver
from utils.validator import Validator


class KanbanBoardService:
    COST_PER_HOUR = 1000

    def __init__(self):
        self.dbms = DBDriver()
        self.validator = Validator()

    def create_task(self, event):
        result = {
            'data': {},
            'status': 201  # Created.
        }
        fields = {
            'title': ['is_set', 'is_empty']
        }
        errors = self.validator.validate(event, result, fields)
        if not errors:
            body = event['body']
            task = Task(title=body['title'])
            session = self.dbms.get_session()
            try:
                session.add(task)
                session.commit()
                result['data'] = self.map_to_json(task)
            except Exception as ex:
                session.rollback()
                result['status'] = 500
                result['data'] = {
                    'errors': {
                        'db': 'session.commit error'
                    }
                }
                print(ex)
            finally:
                session.close()
        else:
            result['data'] = {'errors': errors}
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
            result['status'] = 500
            result['data'] = {
                'errors': {
                    'db': 'session.query.all error'
                }
            }
            print(ex)
        finally:
            session.close()
        return result

    def update_task(self, event):
        body = dict()
        errors = dict()
        result = {
            'data': {},
            'status': 205  # Reset Content.
        }
        fields = {
            'status': ['is_set', 'is_empty']
        }
        id = event['pathParameters']['id']
        if id.isdigit():
            id = int(id)
        else:
            errors['common'] = 'incorrect path'
            result['status'] = 404  # Not Found.
        if not errors:
            errors = self.validator.validate(event, result, fields)
        if not errors:
            body = event['body']
            update = [
                Task.Statuses.TODO.value,
                Task.Statuses.IN_PROGRESS.value,
                Task.Statuses.DONE.value
            ]
            if body['status'] not in update:
                errors['status'] = 'status is unknown'
                result['status'] = 400  # Bad Request.
        if not errors:
            session = self.dbms.get_session()
            try:
                task = session.query(Task).get(id)
                if body['status'] == task.status:
                    errors['status'] = 'status is not changed'
                    result['status'] = 400  # Bad Request.
                elif body['status'] - 1 != task.status:
                    errors['status'] = 'status is incorrect'
                    result['status'] = 409  # Conflict.
                if not errors:
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
                result['status'] = 500
                result['data'] = {
                    'errors': {
                        'db': 'session.commit error'
                    }
                }
                print(ex)
            finally:
                session.close()
        if errors:
            result['data'] = {'errors': errors}
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
