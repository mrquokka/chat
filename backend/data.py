import redis
import sqlalchemy

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
  for message in session.query(Message).all():
    sender_login = message.sender.login
    receiver_login = message.receiver.login
    unique_id = make_unique_chat_id(sender_login, receiver_login)
    if chat_id not in chats:
      chats[chat_id] = {}
    chats[chat_id][message.datetime.timestamp()] = {
      "sender": sender_login,
      "receiver": receiver_login,
    }
  for user in session.query(User).all():
    pipe.hset(KEY_FOR_LOGINGS, user.login, user.hash_password)
  for chat_id, messages in chats.items():
    sorted_messages_times = list(messages.keys()).sort()
    for message_time in sorted_messages_times:
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


def add_session_info(id, login):
  connection.hset(KEY_FOR_SESSIONS, id, login)


def delete_session_info(id):
  connection.hdel(KEY_FOR_SESSIONS, id)


def get_all_chats(current_login):
  result = {}
  logins = connection.hkeys(KEY_FOR_LOGINGS)
  for login in logins:
    result[login] = {}
    for message in connection.hgetall(
      "{}*".format(make_unique_chat_id(current_login, login))
    ):
      print(message)
  return result
