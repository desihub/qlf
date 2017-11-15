from channels import Group
import json
from ui_channel.upstream import start_uptream

# Connected to websocket.connect
def ws_add(message):
    start_uptream()
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the monitor group
    Group("monitor").add(message.reply_channel)
    Group("monitor").send({
        "text": json.dumps({
            "status": "connected"
        })
    })

# Connected to websocket.receive
def ws_message(message):
    Group("monitor").send({
        "text": json.dumps({
            "text": "%s" % message.content['text']
        })
    })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("monitor").discard(message.reply_channel)