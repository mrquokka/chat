import json
import os

import flask
from flask_socketio import SocketIO, emit

app = flask.Flask(__name__, static_url_path="")
socketio = SocketIO(app, async_mode=async_mode)

STATIC_DIR = os.path.join(os.getcwd(), "static")

# Отдача главной страницы, если не найдено в статике
@app.route("/", methods=["GET"], defaults={"useless_error": ""})
@app.errorhandler(404)
def index(useless_error):
  return flask.send_from_directory(STATIC_DIR, "index.html"), 200


@app.route("/api", methods=["POST"])
def api_handler():
  try:
    data = json.loads(flask.request.data.decode("utf-8"))
    print(json.dumps(data, indent=2))
    raise AttributeError("stop")
  except Exception as error:
    # TODO журнал ошибок/взломов
    return "3123123", 403


@socketio.event
def my_event(message):
  emit("my response", {"data": "got it!"})


# Этот код нужен только для дебага (если nginx/nodejs не запущен)
#   поэтому не очень красивый
@app.route("/", defaults={"path2": "", "path3": ""}, methods=["GET"])
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


if __name__ == "__main__":
  app.run(debug=True)
  socketio.run(app, debug=True)
