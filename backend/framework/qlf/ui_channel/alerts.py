import os
import math
import datetime
import json
from util import get_config

cfg = get_config()

disk_percent_warning = cfg.get('main', 'disk_percent_warning')
disk_percent_alert = cfg.get('main', 'disk_percent_alert')


class Alerts:
    def available_space(self):
        statvfs = os.statvfs('./')
        available_space = statvfs.f_frsize * statvfs.f_bavail
        total_space = statvfs.f_frsize * statvfs.f_blocks
        percent_free = int(available_space/total_space*100)
        notification_type = None
        if percent_free < int(disk_percent_warning):
            notification_type = "Warning"
        if percent_free < int(disk_percent_alert):
            notification_type = "Alert"
        notification = json.dumps({
            "text": "Available Disk Space {}%".format(
                percent_free
            ),
            "type": notification_type,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        })
        if notification_type is not None:
            return notification
