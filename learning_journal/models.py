import datetime
from passlib.context import CryptContext
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
password_context = CryptContext(schemes=['pbkdf2_sha512'])

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
        """Return an entry with id."""
        Entry = class_
        entry_q = DBSession.query(Entry)
        entry_q = entry_q.get(id)
        return entry_q

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)

    def verify_password(self, password):
        return password_context.verify(password, self.password)

    @classmethod
    def by_name(class_, name):
        """Return an user with the id."""
        User = class_
        user_q = DBSession.query(User)
        user_q = user_q.filter(User.name == name).first()
        return user_q

