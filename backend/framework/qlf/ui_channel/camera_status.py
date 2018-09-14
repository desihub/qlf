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
            camera = Camera(camera_name)
            self.update_qa_state(camera, log)
            self.cameras.append(camera)
        else:
            try:
                self.update_qa_state(camera, log)
            except Exception as e:
                logger.info(e)

    def update_camera_status(self):
        for camera_name in self.qlf_state.camera_logs.keys():
            try:
                log = self.qlf_state.camera_logs[camera_name]
                self.update_petals(camera_name, log)
                camera = self.find_camera(camera_name)
                if not camera: return

                if "Pipeline completed. Final result" in str(log) \
                        and camera.get_step_status('skysubs') is 'processing_stage':

                    camera.set_step_status('skysubs', 'success_stage')
                    camera.set_step_status('fiberfl', 'success_stage')
                    camera.set_step_status('extract', 'success_stage')
                    camera.set_step_status('preproc', 'success_stage')

                if "Starting to run step SkySub_QL" in str(log) \
                        and camera.get_step_status('skysubs') is 'none':

                    camera.set_step_status('skysubs', 'processing_stage')

                    if "CRITICAL" in str(log) or "Error" in str(log):
                        camera.set_step_status('fiberfl', 'error_stage')
                    else:
                        camera.set_step_status('extract', 'success_stage')
                        camera.set_step_status('fiberfl', 'success_stage')

                if "Starting to run step ApplyFiberFlat_QL" in str(log) \
                        and camera.get_step_status('fiberfl') is 'none':

                    camera.set_step_status('fiberfl', 'processing_stage')

                    if "CRITICAL" in str(log) or "Error" in str(log):
                        camera.set_step_status('extract', 'error_stage')
                    else:
                        camera.set_step_status('extract', 'success_stage')

                if "Starting to run step BoxcarExtract" in str(log) \
                        and camera.get_step_status('extract') is 'none':

                    camera.set_step_status('extract', 'processing_stage')

                    if "CRITICAL" in str(log) or "Error" in str(log):
                        camera.set_step_status('preproc', 'error_stage')
                    else:
                        camera.set_step_status('preproc', 'success_stage')

                if "Starting to run step Initialize" in str(log) \
                        and camera.get_step_status('preproc') is 'none':
                    camera.set_step_status('preproc', 'processing_stage')

                if "CRITICAL" in str(log) or "Error" in str(log) \
                        and camera.get_step_status('preproc') is 'none':
                    camera.set_step_status('preproc', 'error_stage')

            except Exception as err:
                logger.warn(err)

    def format_camera_stage_results(self):
        result = {"r": [], "b": [], "z": []}
        for camera in self.cameras:
            for band in result.keys():
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
