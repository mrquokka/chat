import flask
import flask_socketio

from config import CRYPT_KEY


app = flask.Flask(__name__, static_url_path="")
socketio = flask_socketio.SocketIO(
  app, async_mode="gevent", namespace="/socket", logger=True
)

app.config.update(
  {
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_SECURE": True,
    "SECRET_KEY": CRYPT_KEY,
  }
)
