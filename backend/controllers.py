import json
import os


import flask
from flask_socketio import SocketIO, emit, ConnectionRefusedError

# TODO absolute import
from config import NAMESPACE, STATIC_DIR
from crypt import crypter, get_hash_of_password
from app import app, socketio
from data import (
  add_user,
  get_login_hash,
  add_session_info,
  delete_session_info,
  get_all_chats,
  add_message,
)


# TODO real ban
def make_ban(error):
  print(error)
  return "error"


# Отдача главной страницы, если не найдено в статике
@app.route("/", methods=["GET"], defaults={"useless_error": ""})
@app.errorhandler(404)
def index(useless_error):
  return flask.send_from_directory(STATIC_DIR, "index.html"), 200


def login_and_register(action, data):
  login = str(data["login"])
  password = str(data["password"])
  if not login or not password:
    raise AttributeError("hack?")
  if action == "login":
    hash_password = get_login_hash(login)
    if hash_password:
      is_have_auth_error = hash_password != get_hash_of_password(password)
    else:
      is_have_auth_error = True
    if is_have_auth_error:
      return "invalid password"
  # register block
  elif get_login_hash(login):
    return "error_is_busy"
  else:
    add_user(login, get_hash_of_password(password))
  cookie = crypter.encrypt(login.encode("utf-8")).decode("utf-8")
  response = flask.make_response(login)
  response.set_cookie("login", value=cookie)
  return response


def send_message(sender, receiver, message):
  if not sender or not receiver or not message:
    raise AttributeError("hack attempt?")
  unique_id, unix_time, data = add_message(sender, receiver, message)
  data["unix_time"] = unix_time
  socketio.emit(
    "new_message",
    data,
    to=unique_id,
    include_self=True,
    namespace=NAMESPACE,
  )
  return "OK"


@app.route("/api", methods=["POST"])
def api_handler():
  # try:
  data = json.loads(flask.request.data.decode("utf-8"))
  print(json.dumps(data, indent=2))
  action = data.pop("action")
  if action in ["login", "register"]:
    return login_and_register(action, data)
  login = get_login_from_cookie()
  if not login:
    raise AttributeError("unathorized user")
  if action == "logout":
    response = flask.make_response("OK")
    response.delete_cookie("login")
    return response
  elif action == "get_login":
    return login
  elif action == "get_chats":
    result = get_all_chats(login)
    print(login, result)
    return result
  elif action == "send_message":
    return send_message(login, data.get("receiver"), data.get("message"))
  raise ValueError("unknown path")
  # except Exception as error:
  #   return make_ban(error)


# Этот код нужен только для дебага (если nginx/nodejs не запущен)
#   поэтому не очень красивый
@app.route("/", defaults={"path2": "", "path3": ""}, methods=["GET"])
@app.route(
  "/favicon.ico",
  defaults={"path2": "favicon.ico", "path3": ""},
  methods=["GET"],
)
@app.route("/<path:path2>", defaults={"path3": ""}, methods=["GET"])
@app.route("/<path:path2>/<path:path3>", methods=["GET"])
def send_static(path2, path3):
  result_path = [STATIC_DIR]
  for item in path2, path3:
    if item:
      result_path.append(item)
  return flask.send_from_directory(
    os.path.join(*result_path[:-1]), result_path[-1]
  )


def get_login_from_cookie():
  login_cookie = flask.request.cookies.get("login")
  if login_cookie:
    try:
      login = crypter.decrypt(login_cookie.encode("utf-8")).decode("utf-8")
      if login:
        hash = get_login_hash(login)
        sid = getattr(flask.request, "sid", None)
        if not hash:
          raise AttributeError("deleted account")
        elif sid:
          add_session_info(sid, login)
        return login
    except Exception as error:
      make_ban(error)


@socketio.on("connect", namespace=NAMESPACE)
def test_connect(auth=None):
  if get_login_from_cookie():
    return "OK"
  else:
    raise ConnectionRefusedError("need_login")


@socketio.on("disconnect", namespace=NAMESPACE)
def test_disconnect():
  delete_session_info(flask.request.sid)
