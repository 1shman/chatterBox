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

@app.route("/", methods=["GET", "POST"])
def show_index(): 
    flask.session.clear()
    if flask.request.method == "POST":
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
    
    return flask.render_template("home.html")

@app.route("/room")
def show_room():
    #sanity check 
    room = flask.session.get("room")
    name = flask.session.get("name")
    if room is None or name is None or room not in rooms:
        return flask.redirect(flask.url_for("show_index")) #bug issues/resolved

    return flask.render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data): 
    room = flask.session.get("room")
    if room not in rooms: 
        return
    
    content = {"name": flask.session.get("name"), "message": data["data"]}
    flask_socketio.send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{flask.session.get('name')} said: {data['data']}")
    #TODO: use python library to store time the message was sent

@socketio.on("connect")
def connect(auth):
    room = flask.session.get("room")
    name = flask.session.get("name")
    if not room or not name: 
        return
    if room not in rooms: 
        flask_socketio.leave_room(room)
        return
    
    flask_socketio.join_room(room)
    flask_socketio.send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = flask.session.get("room")
    name = flask.session.get("name")
    flask_socketio.leave_room(room)

    if room in rooms: 
        rooms[room]["members"] -= 1
        if rooms[room]["members"] < 1:
            del rooms[room]
    flask_socketio.send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} left room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)

#TODO: dynamic styled pages
#TODO: adjust input textbox style/dynamic growth for room.html
#TODO: enter button for send message
#TODO: use python library to store time the message was sent