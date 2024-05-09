import flask 
import flask_socketio
import string

#TODO: review boilerplate
app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "filler"
socketio = flask_socketio.SocketIO(app)

@app.route("/", methods=["GET"])
def show_index(): 
    return flask.render_template("home.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)