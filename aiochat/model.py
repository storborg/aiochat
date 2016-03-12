from datetime import datetime

from sqlalchemy import Column, types, orm
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
Session = orm.sessionmaker(autoflush=False)


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(types.Integer, primary_key=True)
    origin = Column(types.String(255), nullable=False)
    name = Column(types.String(255), nullable=False)
    body = Column(types.String(255), nullable=False)
    timestamp = Column(types.DateTime, nullable=False, default=datetime.utcnow)
