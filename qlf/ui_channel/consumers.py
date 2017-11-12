from channels import Group

# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the monitor group
    Group("monitor").add(message.reply_channel)
    Group("monitor").send({
        "text": "teste",
    })

# Connected to websocket.receive
def ws_message(message):
    Group("monitor").send({
        "text": "%s" % message.content['text'],
    })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("monitor").discard(message.reply_channel)