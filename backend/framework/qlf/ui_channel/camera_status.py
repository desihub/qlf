import os
import configparser
import copy
import logging
from log import get_logger
from ui_channel.alerts import Alerts
from ui_channel.camera import Camera

desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
qlf_root = os.getenv('QLF_ROOT')

logger = get_logger(
    "qlf.camera_status",
    os.path.join(qlf_root, "logs", "camera_status.log")
)


class CameraStatus:
    def __init__(self, qlf_state):
        self.reset_camera_status()
        self.alerts = Alerts()
        self.qlf_state = qlf_state

    def reset_camera_status(self):
        self.cameras = list()

    def update_qa_state(self, camera, log):
        for line in log:
            for alert_key in camera.alert_keys:
                if alert_key in line and camera.get_qa_status(alert_key) is 'None':
                    status = line.split(
                        '{}:'.format(alert_key)
                    )[1][1:-1]
                    camera.set_qa_status(alert_key, status)
                    if status != 'NORMAL':
                        self.alerts.qa_alert(
                            camera.name, alert_key, status, self.qlf_state.exposure_id)

    def find_camera(self, camera_name):
        for camera in self.cameras:
            if camera_name in camera.name:
                return camera
        return None

    def update_petals(self, camera_name, log):
        camera = self.find_camera(camera_name)

        if camera is None:
            camera = Camera(camera_name, self.qlf_state.stages)
            self.update_qa_state(camera, log)
            self.cameras.append(camera)
        else:
            try:
                self.update_qa_state(camera, log)
            except Exception as e:
                logger.info(e)

    def update_camera_status(self):
        for camera_name in list(self.qlf_state.camera_logs):
            try:
                log = self.qlf_state.camera_logs[camera_name]
                self.update_petals(camera_name, log)
                camera = self.find_camera(camera_name)
                if not camera: return

                for step in self.qlf_state.stages['step_list']:
                    if "CRITICAL" in str(log) and \
                            camera.get_step_status(step['name']) is 'processing_stage':
                        camera.set_step_status(step['name'], 'error_stage')
                    if step['start'] in str(log) and \
                            camera.get_step_status(step['name']) is 'none':
                        camera.set_step_status(step['name'], 'processing_stage')
                    if step['end'] in str(log) and \
                            camera.get_step_status(step['name']) is 'processing_stage':
                        camera.set_step_status(step['name'], 'success_stage')

            except Exception as err:
                logger.warn(err)

    def format_camera_stage_results(self):
        result = {"r": [], "b": [], "z": []}
        for camera in self.cameras:
            for band in list(result):
                if band in camera.name:
                    result[band].append({camera.name[1:]: camera.steps_status})
        return result

    def get_camera_status(self):
        self.update_camera_status()
        return self.format_camera_stage_results()

    def get_qa_petals(self):
        result = []
        for camera in self.cameras:
            result.append({ camera.name: camera.qas_status })
        return result
