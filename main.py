import flask 
import flask_socketio
import random
import string

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "filler"
socketio = flask_socketio.SocketIO(app)

rooms = {}

def codeGenerator(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(string.ascii_lowercase)
        if code not in rooms: 
            break
    return code

@app.route("/", methods=["GET"])
def show_index(): 
    flask.session.clear()
    return flask.render_template("home.html")

@app.route("/", methods=["POST"])
def post_index(): 
    name = flask.request.form.get("name")
    roomCode = flask.request.form.get("roomCode")
    join = flask.request.form.get("join", False)
    create = flask.request.form.get("create", False)

    #error checking
    if not name: 
        return flask.render_template("home.html", error="Please enter your name.", roomCode=roomCode, name=name)
    #TODO: revist join != false
    if join != False and not roomCode: 
        return flask.render_template("home.html", error="Please enter a room code.", roomCode=roomCode, name=name)
    
    room = roomCode
    if create != False:
        room = codeGenerator(4)
        rooms[room] = {"members": 0, "messages": []}

    elif roomCode not in rooms:
        return flask.render_template("home.html", error="Room Does not exist.", roomCode=roomCode, name=name)

    flask.session["room"] = room
    flask.session["name"] = name

    return flask.redirect(flask.url_for("show_room"))

@app.route("/room")
def show_room(): 
    return flask.render_template("room.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)