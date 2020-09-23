from models.task import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class KanbanBoardService:
    COST_PER_HOUR = 1000

    def get_tasks(self, event):
        result = {
            'data': {},
            'status': 200  # OK.
        }
        engine = self.get_engine()
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        tasks = session.query(Task).all()
        objects = []
        if tasks:
            for task in tasks:
                obj = self.map_to_json(task)
                objects.append(obj)
        result['data'] = objects
        return result

    def get_engine(self):
        return create_engine(
            'postgresql+pg8000://'
            + 'postgres:postgresrootpass'
            + '@'
            + 'localhost:5432/kanban_board',
            client_encoding='utf8'
        )

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
            obj['start_time'] = task.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if task.end_time:
            obj['end_time'] = task.end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return obj
