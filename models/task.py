from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import SmallInteger
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class Task(Base):
    """Task."""

    class Statuses(enum.Enum):
        TODO = 0
        IN_PROGRESS = 1
        DONE = 2

    __tablename__ = 'tasks'
    id = Column(SmallInteger, primary_key=True)
    title = Column(String(64), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(SmallInteger, default=0)
    payment = Column(Integer, default=0)
