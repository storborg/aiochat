from sqlalchemy import Column, types
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(types.Integer, primary_key=True)
    body = Column(types.String(255), nullable=False)
