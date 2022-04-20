import threading

import sqlalchemy
import sqlalchemy.orm


Base = sqlalchemy.orm.declarative_base()
engine = sqlalchemy.create_engine(
  "postgresql://postgres:postgres@localhost/chat"
)
lock = threading.Lock()


class User(Base):
  __tablename__ = "user"
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  login = sqlalchemy.Column(sqlalchemy.String)
  hash_password = sqlalchemy.Column(sqlalchemy.String)


class Message(Base):
  __tablename__ = "message"
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  description = sqlalchemy.Column(sqlalchemy.String)
  is_readed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
  datetime = sqlalchemy.Column(sqlalchemy.DateTime)
  sender_id = sqlalchemy.Column(
    sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id")
  )
  sender = sqlalchemy.orm.relationship(
    "User", foreign_keys=[sender_id], backref="sended_messages"
  )
  receiver_id = sqlalchemy.Column(
    sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id")
  )
  receiver = sqlalchemy.orm.relationship(
    "User", foreign_keys=[receiver_id], backref="received_messages"
  )
