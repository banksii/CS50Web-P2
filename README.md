# Project 2

Web Programming with Python and JavaScript

index.html index.js
This is the default page which requests the visitor to select a username.  The JS code queries the server to check that the username is available.  If it isn't then the visitor is notified to choose another name.  If it is available the user is re-directed to the home.html page.  If the the visitor has visted before and has a username stored in local storage then the they are automatically re-directed to the home.html page before the index.html page is loaded.  Likewise, if they have both a username and channel stored in localstorage then they are re-directed to the appropriate channel page before the index.html page is loaded.

home.html home.js
This page offers the visitor a list of available channels in addition to the option of creating a new channel.  When the channel creation form is submitted the JS code queries the server to see if the name is available.  If it isn't then the visitor is notified to choose a different channel name.  If it is available the user is re-directed to a dynamically created channel page at /channel/<channel name>.

channel.html channel.js
This is the template that is used to dynamically create each channel page at /channel/<channel name>.  The JS code connects the socketIO and listens for new messages as well as sending any messages input by the user (although it does not allow empty messages to be sent).  It also notifies the server when the user joins or leaves the channel (using join_room and leave_room functions from flask_socketio.  Since the server knows which users are in which channel, messages broadcast from the server are only sent to the users in the same room as the message sender.  I have also used this to associate each user with a channel in a dictionary global variable of users on the server.  This allows a list of users in each channel to be displayed on the right hand side of the channel page and be dynamically updated as users join and leave the room.  This is the personal touch of my project

layout.html layout.js
This holds the basic page layout and nav and generates the list of channels, which are automatically hidden if a visitor is not registered.  The channel list is dynamically updated such that when a new channel is created, socket.io is used to updated all clients.  This is another personal touch of my project

application.py
The list of users is tracked in a dictionary where the username is the key and the current room they are in is stored as the value.  All messages sent are stored in a single dictionary where the channel name is the key and the value is a list of message dictionaries, each containing the user, text and timestamp of each message.  The list of messages for each channel is limited to 100.  Once this limit is reached the first message in the list if removed.  This is checked each time the server recevies a new message from a client. Note that as per the requirements a user joining a channel is shown all the messages stored on the server for that channel (which is always going to be 100 or fewer), however as new messages are sent the clients view does not limit the number of messages displayed to 100 - this was not listed as a requirement in the project description. 

Personal touch
As described above the personal touches are a dynamically updated list of users in the channel and dynamically updated list of channels as they are created.