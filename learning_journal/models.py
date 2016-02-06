import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    DateTime,
    desc
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(Text)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow())
    
    @classmethod
    def all(class_):
        """Return a query of all entries."""
        Entry = class_
        entry_q = DBSession.query(Entry)
        entry_q = entry_q.order_by(desc(Entry.created))
        return entry_q

    @classmethod
    def by_id(class_, id):
        """Return a query of entries sorted by id."""
        Entry = class_
        entry_q = DBSession.query(Entry)
        entry_q = entry_q.get(id)
        return entry_q

