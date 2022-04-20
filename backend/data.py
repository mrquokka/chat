import datetime
import json

import redis
import sqlalchemy
import flask_socketio

from config import NAMESPACE
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
      "is_readed": message_obj.is_readed,
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


def add_user(new_login, hash_password):
  lock.acquire()
  with sqlalchemy.orm.Session(engine) as session:
    session.add(User(login=new_login, hash_password=hash_password))
    session.commit()
  connection.hset(KEY_FOR_LOGINGS, new_login, hash_password)
  for sid, login in connection.hgetall(KEY_FOR_SESSIONS).items():
    flask_socketio.join_room(
      make_unique_chat_id(new_login, login), sid=sid, namespace=NAMESPACE
    )
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
    for unix_time, description in connection.hgetall(unique_id).items():
      result[login][unix_time] = json.loads(description)
  return result


def add_message(sender, receiver, message):
  current_date = datetime.datetime.now()
  lock.acquire()
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
      is_readed=False,
    )
    unique_id, unix_time, data = get_message_info(message_obj)
    connection.hset(unique_id, unix_time, json.dumps(data))
    session.add(message_obj)
    session.commit()
  lock.release()
  return unique_id, unix_time, data


def mark_readed_messages(messages_infos):
  messages_to_read = {}
  lock.acquire()
  pipe = connection.pipeline()
  with sqlalchemy.orm.Session(engine) as session:
    for item in messages_infos:
      sender = item["sender"]
      receiver = item["receiver"]
      timestamp = item["timestamp"]
      alias_sender = sqlalchemy.orm.aliased(User)
      alias_receiver = sqlalchemy.orm.aliased(User)
      message_date = datetime.datetime.fromtimestamp(float(timestamp))
      message = (
        session.query(Message)
        .join(alias_sender, Message.sender)
        .join(alias_receiver, Message.receiver)
        .filter(
          sqlalchemy.and_(
            alias_sender.login == sender,
            alias_receiver.login == receiver,
            Message.datetime == message_date,
          )
        )
        .first()
      )
      if not message:
        raise AttributeError("hack attempt?")
      if not message.is_readed:
        message.is_readed = True
        unique_id = make_unique_chat_id(sender, receiver)
        if unique_id not in messages_to_read:
          messages_to_read[unique_id] = []
        messages_to_read[unique_id].append(
          {"timestamp": timestamp, "sender": sender, "receiver": receiver}
        )
        _1, _2, data = get_message_info(message)
        pipe.hset(unique_id, timestamp, json.dumps(data))
    session.commit()
  pipe.execute()
  lock.release()
  return messages_to_read
