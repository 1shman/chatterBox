import flask 
import flask_socketio
import string

#TODO: review this
app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "filler"
socketio = flask_socketio.SocketIO(app)

if __name__ == "__main__":
    socketio.run(app, debug=True)