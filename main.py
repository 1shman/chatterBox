import flask 
import flask_socketio
import string

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "filler"
socketio = flask_socketio.SocketIO(app)

@app.route("/", methods=["GET"])
def show_index(): 
    return flask.render_template("home.html")

@app.route("/", methods=["POST"])
def get_index(): 
    name = flask.request.form.get("name")
    roomCode = flask.request.form.get("roomCode")
    join = flask.request.form.get("join", False)
    create = flask.request.form.get("create", False)

    #error checking
    if not name: 
        return flask.render_template("home.html", error="Please enter your name.")
    #TODO: revist join != false
    if join != False and not roomCode: 
        return flask.render_template("home.html", error="Please enter a room code.")
    
    room = roomCode
    if create != False:
        room = 0000

    return flask.render_template("room.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)