import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBDriver:
    """High-level database driver"""

    def __init__(self):
        self.dbms = False

    def _create_engine(self):
        if 'USER' in os.environ:
            user = 'postgres'
            passwd = 'postgresrootpass'
            host = 'localhost'
            port = '5432'
            dbname = 'kanban_board_sls'
        else:
            user = os.environ['user']
            passwd = os.environ['pass']
            host = os.environ['host']
            port = str(os.environ['port'])
            dbname = os.environ['dbname']

        fuel = 'postgresql+pg8000://' + user + ':' + passwd + '@'
        fuel += host + ':' + port + '/' + dbname
        self.dbms = create_engine(fuel, client_encoding='utf8')

    def get_dbms(self):
        if not self.dbms:
            self._create_engine()
        return self.dbms

    def get_session(self):
        dbms = self.get_dbms()
        session_factory = sessionmaker(bind=dbms)
        return session_factory()
