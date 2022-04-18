import threading

import sqlalchemy

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = sqlalchemy.create_engine(
  "postgresql://postgres:postgres@localhost/chat"
)
lock = threading.Lock()


class User(Base):
  __tablename__ = "user"
  id = Column(Integer, primary_key=True)
  login = Column(String)
  hash_password = Column(String)


class Message(Base):
  __tablename__ = "message"
  id = Column(Integer, primary_key=True)
  login = Column(String)
  datetime = Column(sqlalchemy.DateTime)
  sender_id = Column(Integer, ForeignKey("user.id"))
  sender = relationship(
    "User", foreign_keys=[sender_id], backref="sended_messages"
  )
  receiver_id = Column(Integer, ForeignKey("user.id"))
  receiver = relationship(
    "User", foreign_keys=[receiver_id], backref="received_messages"
  )
