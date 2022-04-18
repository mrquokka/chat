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


@app.route("/api", methods=["POST"])
def api_handler():
  # try:
  data = json.loads(flask.request.data.decode("utf-8"))
  action = data.pop("action")
  login = str(data["login"])
  password = str(data["password"])
  print(action, login, password)
  if not login or not password:
    raise AttributeError("hack?")
  if action == "login":
    hash_password = get_login_hash(login)
    print(hash_password, get_hash_of_password(password))
    if not hash_password:
      return "invalid password"
    # TODO убрать дублирование, но пока не придумал как лучше
    elif hash_password != get_hash_of_password(password):
      return "invalid password"
  # register block
  elif get_login_hash(login):
    return "error_is_busy"
  else:
    add_user(login, get_hash_of_password(password))
  cookie = crypter.encrypt(login.encode("utf-8")).decode("utf-8")
  response = flask.make_response("OK")
  response.set_cookie("login", value=cookie)
  return response


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
  print(path2, path3)
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
        if hash:
          add_session_info(flask.request.sid, login)
          return login
    except Exception as error:
      make_ban(error)


@socketio.on("connect", namespace=NAMESPACE)
@socketio.on("get_login", namespace=NAMESPACE)
def test_connect(auth=None):
  login_from_cookie = get_login_from_cookie()
  if login_from_cookie:
    return login_from_cookie
  else:
    raise ConnectionRefusedError("need_login")


@socketio.on("disconnect", namespace=NAMESPACE)
def test_disconnect():
  delete_session_info(flask.request.sid)


@socketio.event(namespace=NAMESPACE)
def get_chats(*args):
  login_from_cookie = get_login_from_cookie()
  if login_from_cookie:
    return get_all_chats(login_from_cookie)
  else:
    raise ConnectionRefusedError("need_login")


# @socketio.event(namespace=NAMESPACE)
# def register(sended_data):
