import datetime
import json

import redis
import sqlalchemy
import flask_socketio

from db import lock, User, Message, engine, Base

# TODO postgres + sqlalchemy
connection = redis.Redis(
  host="localhost", port=6379, db=0, decode_responses=True
)
KEY_FOR_LOGINGS = "logins"
KEY_FOR_SESSIONS = "sessions"
PREFIX_FOR_CHATS = "chat"


def make_unique_chat_id(login1, login2):
  logins = [login1, login2]
  logins.sort()
  return "{}_{}".format(PREFIX_FOR_CHATS, "_".join(logins))


def get_message_info(message_obj):
  sender_login = message_obj.sender.login
  receiver_login = message_obj.receiver.login
  unique_id = make_unique_chat_id(sender_login, receiver_login)
  unix_time = message_obj.datetime.timestamp()
  return (
    unique_id,
    unix_time,
    {
      "sender": sender_login,
      "receiver": receiver_login,
      "message": message_obj.description,
    },
  )


# Полная очистка
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# connection.delete(KEY_FOR_LOGINGS)
# connection.delete(KEY_FOR_SESSIONS)

# Очистка только кэша
connection.flushdb()
with sqlalchemy.orm.Session(engine) as session:
  chats = {}
  pipe = connection.pipeline()
  for message_obj in session.query(Message).all():
    unique_id, unix_time, data = get_message_info(message_obj)
    if unique_id not in chats:
      chats[unique_id] = {}
    chats[unique_id][unix_time] = json.dumps(data)
  for user in session.query(User).all():
    pipe.hset(KEY_FOR_LOGINGS, user.login, user.hash_password)
  for chat_id, messages in chats.items():
    unix_times = list(messages.keys())
    unix_times.sort()
    for message_time in unix_times:
      pipe.hset(chat_id, message_time, messages[message_time])
  pipe.execute()


def add_user(login, hash_password):
  lock.acquire()
  with sqlalchemy.orm.Session(engine) as session:
    session.add(User(login=login, hash_password=hash_password))
    session.commit()
  connection.hset(KEY_FOR_LOGINGS, login, hash_password)
  lock.release()


def get_login_hash(login):
  return connection.hget(KEY_FOR_LOGINGS, login)


def get_all_logins():
  return connection.hkeys(KEY_FOR_LOGINGS)


def add_session_info(id, current_login):
  connection.hset(KEY_FOR_SESSIONS, id, current_login)
  for login in get_all_logins():
    flask_socketio.join_room(make_unique_chat_id(current_login, login))


def delete_session_info(id):
  current_login = connection.hget(KEY_FOR_SESSIONS, id)
  connection.hdel(KEY_FOR_SESSIONS, id)

  for login in get_all_logins():
    flask_socketio.leave_room(make_unique_chat_id(current_login, login))


def get_all_chats(current_login):
  result = {}
  logins = get_all_logins()
  for login in logins:
    result[login] = {}
    unique_id = make_unique_chat_id(current_login, login)
    for unix_time in connection.hgetall(unique_id):
      description = connection.hget(unique_id, unix_time)
      result[login][unix_time] = json.loads(description)
  return result


def add_message(sender, receiver, message):
  current_date = datetime.datetime.now()
  with sqlalchemy.orm.Session(engine) as session:
    sender = session.query(User).filter(User.login == sender).first()
    receiver = session.query(User).filter(User.login == receiver).first()
    if not sender or not receiver:
      raise AttributeError("unknown users")
    message_obj = Message(
      description=message,
      datetime=current_date,
      sender=sender,
      receiver=receiver,
    )
    unique_id, unix_time, data = get_message_info(message_obj)
    connection.hset(unique_id, unix_time, json.dumps(data))
    session.add(message_obj)
    session.commit()
    return unique_id, unix_time, data