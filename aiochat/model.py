import time
from datetime import datetime

from sqlalchemy import Column, types, orm, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
Session = orm.scoped_session(orm.sessionmaker())


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(types.Integer, primary_key=True)
    origin = Column(types.String(255), nullable=False)
    name = Column(types.String(255), nullable=False)
    body = Column(types.String(255), nullable=False)
    timestamp = Column(types.DateTime, nullable=False, default=datetime.utcnow)


def init(url):
    print("Initializing DB...")
    engine = create_engine(url)
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    print("DB ready.")


def record_message(addr, name, body):
    time.sleep(10)
    msg = Message(origin=addr, name=name, body=body)
    Session.add(msg)
    Session.commit()
