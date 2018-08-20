import os
import math
import datetime
import json
from clients import get_ics_daemon
from channels import Group

disk_percent_warning = os.environ.get('DISK_SPACE_PERCENT_WARNING')
disk_percent_alert = os.environ.get('DISK_SPACE_PERCENT_ALERT')


class Alerts:
    def qa_alert(self, camera, qa, status, exposure_id):
        notification_type = status
        notification = json.dumps({
            "text": "Exposure {}: {} {} {}".format(
                exposure_id,
                camera,
                qa,
                status,
            ),
            "type": notification_type,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        })
        if notification_type is not None:
            Group("monitor").send({
                "text": json.dumps({
                    "notification": notification
                })
            })

    def available_space(self):
        statvfs = os.statvfs('./')
        available_space = statvfs.f_frsize * statvfs.f_bavail
        total_space = statvfs.f_frsize * statvfs.f_blocks
        percent_free = int(available_space/total_space*100)
        notification_type = None
        if percent_free < int(disk_percent_warning):
            notification_type = "WARNING"
        if percent_free < int(disk_percent_alert):
            notification_type = "ALARM"

        if os.environ.get('START_ICS', 'False') is 'True':
            self.notify_ics("Available Disk Space {}%".format(
                    percent_free
            ))

        notification = json.dumps({
            "text": "Available Disk Space {}%".format(
                percent_free
            ),
            "type": notification_type,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        })
        if notification_type is not None:
            return notification

    def notify_ics(self, message):
        ics = get_ics_daemon()
        ics.alert(message)
