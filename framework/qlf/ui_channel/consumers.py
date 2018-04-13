from channels import Group
import json
from ui_channel.upstream import start_uptream, start_daemon, stop_daemon,\
    reset_daemon, get_camera_log, job, get_current_state, get_current_qa_tests

# Connected to websocket.connect
def ws_add(message):
    start_uptream()
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
        "text": get_current_state()
    })

# Connected to websocket.receive
def ws_message(message):
    if message.content['text'] == "startPipeline":
        start_daemon()
        message.reply_channel.send({
            "text": get_current_state()
        })
        return
    if message.content['text'] == "stopPipeline":
        stop_daemon()
        message.reply_channel.send({
            "text": get_current_state()
        })
        return
    if message.content['text'] == "resetPipeline":
        reset_daemon()
        message.reply_channel.send({
            "text": get_current_state()
        })
        return
    if "camera" in message.content['text']:
        message.reply_channel.send({
            "text": json.dumps({
                "cameralog": get_camera_log(str(message.content['text'].split(":")[1]))
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