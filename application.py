import os
import sys

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users = {"admin": ""} #set(["rob", "kenny"])
#channels = set(["CS50 project 1", "CS50 project 2", "test_limit"])
messages = {
    "CS50 project 1" : [
        {
        "user" : "rob",
        "message" : "this is a test",
        "timestamp" : "1"
        },
        {
        "user" : "rob",
        "message" : "this is another test",
        "timestamp" : "2"
        }        
    ],
    "test_limit" : []
} 
    
# create a channel with 99 messages for testing
for x in range(100):
    messages['test_limit'].append({'user': 'testuser', 'message': x, 'timestamp': x })

def users_list(channel_name):
    return [user for user, channel in users.items() if channel == channel_name] # gets all users that are in a particular channel and puts them in a list


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    # get list of channels
    channels = messages.keys()
    return render_template("home.html", channels=channels)

@app.route("/channel/<channel>")
def channel(channel):

    if channel in messages:
        channels = [*messages] # changed to use list literal method to get list of keys, previously used: messages.keys()
        channels.remove(channel) #remove current channel from list
        #print(messages.keys(), file=sys.stderr)
        return render_template("channel.html", channels=channels, messages=messages[channel], current_channel=channel, users=users_list(channel))

    else:
        return redirect(url_for("home"))

@app.route("/adduser", methods=["POST"])
def adduser():

    # get username submitted from form
    name = request.form.get("username")


    # debug
    print(users, file=sys.stderr)
    # print(name not in users, file=sys.stderr)
    
    # Check username not already taken    
    if name not in users:
        users[name] = "" # add user and set channel to empty string, users.add(name)
        print("TRUE", file=sys.stderr) 
        return jsonify({"success": True}) 
    else:
        print("FALSE", file=sys.stderr)
        return jsonify({"success": False})

@app.route("/addchannel", methods=["POST"])
def addchannel():

    # get channel submitted from form
    channel = request.form.get("channel") 
    
    # Check channel name not already taken TODO get rid of channel set and just check dictionary of messages    
    if channel not in messages:
        messages[channel] = []
        # update channel list on all clients
        socketio.emit("new channel", channel) 
        return jsonify({"success": True}) 
    
    else:
        return jsonify({"success": False})


@socketio.on("submit message")
def message(data):
    message = data["message_data"]
    channel = data["channel"]
    
    # add message to dictionary in correct channel
    # first check if the channel is already in the dictionary (i.e. there are already messages present)
    if channel in messages:

        # want to limit to 100 messages so check length of list before adding
        if len(messages[channel]) < 100:
            messages[channel].append(message)
            print(len(messages[channel]), file=sys.stderr)
        else:
            removed = messages[channel].pop(0) #remove first message (i.e. oldest) in list
            print(removed, file=sys.stderr)
            messages[channel].append(message)
            print(len(messages[channel]), file=sys.stderr)           

    else: # add new key in dictionary for that channel - value is contained in a list, hence square brackets
        messages[channel] = [message]

    emit("new message", message, room=channel) #broadcast=True)

@socketio.on("join")
def on_join(data):
    
    join_room(data["channel"])

    # store current channel against username in user list
    users[data["user"]] = data["channel"]

    # update user list on all clients on that channel
    # socketio.emit("user list", users_list(data["channel"]), room=data["channel"]) 
    socketio.emit("add user", data["user"], room=data["channel"]) 

    print(data["user"] + " joined " + data["channel"], file=sys.stderr)



@socketio.on("leave")
def on_leave(data):

    leave_room(data["channel"])
    disconnect()
    print(users, file=sys.stderr)
    # set channel to "" for that user
    users[data["user"]] = ""

    # update user list on all clients on that channel
    socketio.emit("remove user", data["user"], room=data["channel"]) 
    print(data["user"] + " left " + data["channel"], file=sys.stderr)
    print(users, file=sys.stderr)


# this is required to get socketio to work on development server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

