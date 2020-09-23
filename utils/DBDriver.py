from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBDriver:
    """High-level database driver"""

    def __init__(self):
        self.dbms = False

    def _create_engine(self):
        self.dbms = create_engine(
            'postgresql+pg8000://'
            + 'postgres:postgresrootpass'
            + '@'
            + 'localhost:5432/kanban_board_sls',
            client_encoding='utf8'
        )

    def get_dbms(self):
        if not self.dbms:
            self._create_engine()
        return self.dbms

    def get_session(self):
        dbms = self.get_dbms()
        session_factory = sessionmaker(bind=dbms)
        return session_factory()
