from channels import Group
import json
from ui_channel.upstream import Upstream

us = Upstream()

# Connected to websocket.connect
def ws_add(message):
    us.start_uptream()
    # Accept the connection
    message.reply_channel.send({"accept": True})
    message.reply_channel.send({
        "text": json.dumps({
            "status": "connected"
        })
    })
    # Add to the monitor group
    Group("monitor").add(message.reply_channel)
    message.reply_channel.send({
        "text": json.dumps({
            "status": "connected monitor"
        })
    })

# Connected to websocket.receive
def ws_message(message):
    if message.content['text'] == "startPipeline":
        us.start_daemon()
        message.reply_channel.send({
            "text": us.get_current_state()
        })
        return
    if message.content['text'] == "stopPipeline":
        us.stop_daemon()
        message.reply_channel.send({
            "text": us.get_current_state()
        })
        return
    if message.content['text'] == "resetPipeline":
        us.reset_daemon()
        message.reply_channel.send({
            "text": us.get_current_state()
        })
        return
    # Get Single Camera
    if "camera" in message.content['text']:
        message.reply_channel.send({
            "text": json.dumps({
                "cameralog": us.get_camera_log(str(message.content['text'].split(":")[1]))
            })
        })
    # User Channel
    if "uuid" in message.content['text']:
        Group(str(message.content['text'].split("uuid=")[1])).add(message.reply_channel)

        Group(str(message.content['text'].split("uuid=")[1])).send({
            "text": json.dumps({
                "text": "Test single channel"
            })
        })

    Group("monitor").send({
        "text": json.dumps({
            "text": "%s" % message.content['text']
        })
    })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("monitor").discard(message.reply_channel)