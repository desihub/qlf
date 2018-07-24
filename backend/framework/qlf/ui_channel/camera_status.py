import os
import configparser
import copy
import logging
from log import get_logger
from util import get_config
from ui_channel.alerts import Alerts

cfg = get_config()
qlf_root = cfg.get("environment", "qlf_root")

logger = get_logger(
    "qlf.camera_status",
    os.path.join(qlf_root, "logs", "camera_status.log")
)

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

try:
    cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
except Exception as error:
    logger.error(error)
    logger.error("Error reading  %s/framework/config/qlf.cfg" % qlf_root)


class CameraStatus:
    def __init__(self, qlf_state):
        self.reset_camera_status()
        self.alerts = Alerts()
        self.qlf_state = qlf_state

    def reset_camera_status(self):
        self.cams_stages_r = list()
        for i in range(4):
            self.cams_stages_r.append(
                    dict(camera=[i for i in range(10)])
            )

            self.cams_stages_b = copy.deepcopy(self.cams_stages_r)
            self.cams_stages_z = copy.deepcopy(self.cams_stages_r)

        self.qa_petals = list()

    def update_qa_state(self, camera, cam, log, cam_index):
        contains_status = False
        for line in log:
            if 'BIAS_STATUS' in line:
                contains_status = True
                status = line.split(
                    'BIAS_STATUS:'
                )[1][1:-1]

                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['preproc']['steps_status'][1] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'BIAS', status, self.qlf_state.exposure_id)
                camera[cam]['preproc']['steps_status'][1] = status
            elif 'XWSIGMA_STATUS' in line:
                status = line.split(
                    'XWSIGMA_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['preproc']['steps_status'][3] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'XWSIGMA', status, self.qlf_state.exposure_id)
                camera[cam]['preproc']['steps_status'][3] = status
            elif 'LITFRAC_STATUS' in line:
                status = line.split(
                    'LITFRAC_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['preproc']['steps_status'][0] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'COUNTPIX', status, self.qlf_state.exposure_id)
                camera[cam]['preproc']['steps_status'][0] = status
            elif 'NOISE_STATUS' in line:
                status = line.split(
                    'NOISE_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['preproc']['steps_status'][2] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'GETRMS', status, self.qlf_state.exposure_id)
                camera[cam]['preproc']['steps_status'][2] = status
            elif 'NGOODFIB_STATUS' in line:
                status = line.split(
                    'NGOODFIB_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['extract']['steps_status'][0] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'COUNTBINS', status, self.qlf_state.exposure_id)
                camera[cam]['extract']['steps_status'][0] = status
            elif 'SKYCONT_STATUS' in line:
                status = line.split(
                    'SKYCONT_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['fiberfl']['steps_status'][0] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'SKYCONT', status, self.qlf_state.exposure_id)
                camera[cam]['fiberfl']['steps_status'][0] = status
            elif 'PEAKCOUNT_STATUS' in line:
                status = line.split(
                    'PEAKCOUNT_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['fiberfl']['steps_status'][1] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'SKYPEAK', status, self.qlf_state.exposure_id)
                camera[cam]['fiberfl']['steps_status'][1] = status
            elif 'FIDSNR_STATUS' in line:
                status = line.split(
                    'FIDSNR_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['skysubs']['steps_status'][2] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'SNR', status, self.qlf_state.exposure_id)
                camera[cam]['skysubs']['steps_status'][2] = status
            elif 'DELTAMAG_STATUS' in line:
                status = line.split(
                    'DELTAMAG_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['skysubs']['steps_status'][0] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'INTEG', status, self.qlf_state.exposure_id)
                camera[cam]['skysubs']['steps_status'][0] = status
            elif 'RESID_STATUS' in line:
                status = line.split(
                    'RESID_STATUS:'
                )[1][1:-1]
                if len(self.qa_petals) > 0 and \
                    cam_index is not None and \
                    self.qa_petals[cam_index][cam]['skysubs']['steps_status'][1] is 'None' and \
                    status != 'NORMAL':
                    self.alerts.qa_alert(cam, 'SKYRESID', status, self.qlf_state.exposure_id)
                camera[cam]['skysubs']['steps_status'][1] = status

        if not contains_status:
            self.reset_camera_status()

    def update_petals(self, cam, log):
        cam_index = None

        for index, qa_petal in enumerate(self.qa_petals):
            if cam in qa_petal.keys():
                cam_index = index
                break

        camera = None

        if cam_index is None:
            camera = {
                cam: {
                    "extract": {
                        "steps_status": ["None"]
                    },
                    "fiberfl": {
                        "steps_status": ["None", "None"]
                    },
                    "preproc": {
                        "steps_status": ["None", "None", "None", "None"]
                    },
                    "skysubs": {
                        "steps_status": ["None", "None", "None"]
                    }
                }
            }
            self.update_qa_state(camera, cam, log, cam_index)
            self.qa_petals.append(camera)
        else:
            try:
                camera = self.qa_petals[cam_index]
                self.update_qa_state(camera, cam, log, cam_index)
                self.qa_petals[cam_index] = camera
            except Exception as e:
                logger.info(e)

    def update_camera_status(self):
        for cam in self.qlf_state.camera_logs.keys():
            log = self.qlf_state.camera_logs[cam]
            self.update_petals(cam, log)

            if "Pipeline completed. Final result" in ''.join(log):
                self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                self.update_stage(cam[:1], 1, int(cam[1:]), 'success_stage')
                self.update_stage(cam[:1], 2, int(cam[1:]), 'success_stage')
                self.update_stage(cam[:1], 3, int(cam[1:]), 'success_stage')
            elif "Starting to run step SkySub_QL" in ''.join(log):
                self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                self.update_stage(cam[:1], 1, int(cam[1:]), 'success_stage')
                self.update_stage(cam[:1], 2, int(cam[1:]), 'success_stage')
                if "Traceback (most recent call last):" in ''.join(log):
                    self.update_stage(cam[:1], 3, int(cam[1:]), 'error_stage')
                else:
                    self.update_stage(cam[:1], 3, int(cam[1:]), 'processing_stage')
                next

            elif "Starting to run step ApplyFiberFlat_QL" in ''.join(log):
                self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                self.update_stage(cam[:1], 1, int(cam[1:]), 'success_stage')
                if "Traceback (most recent call last):" in ''.join(log):
                    self.update_stage(cam[:1], 2, int(cam[1:]), 'error_stage')
                else:
                    self.update_stage(cam[:1], 2, int(cam[1:]), 'processing_stage')
                next

            elif "Starting to run step BoxcarExtract" in ''.join(log):
                self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                if "Traceback (most recent call last):" in ''.join(log):
                    self.update_stage(cam[:1], 1, int(cam[1:]), 'error_stage')
                else:
                    self.update_stage(cam[:1], 1, int(cam[1:]), 'processing_stage')
                next

            elif "Starting to run step Initialize" in ''.join(log):
                if "Traceback (most recent call last):" in ''.join(log):
                    self.update_stage(cam[:1], 0, int(cam[1:]), 'error_stage')
                else:
                    self.update_stage(cam[:1], 0, int(cam[1:]), 'processing_stage')
                next
            elif "Traceback (most recent call last):" in ''.join(log):
                self.update_stage(cam[:1], 0, int(cam[1:]), 'error_stage')
            else:
                self.update_stage(cam[:1], 0, int(cam[1:]), 'none')
                self.update_stage(cam[:1], 1, int(cam[1:]), 'none')
                self.update_stage(cam[:1], 2, int(cam[1:]), 'none')
                self.update_stage(cam[:1], 3, int(cam[1:]), 'none')

    def update_stage(self, band, stage, camera, status):
        if band == 'r':
            self.cams_stages_r[stage]['camera'][camera] = status
        if band == 'z':
            self.cams_stages_z[stage]['camera'][camera] = status
        if band == 'b':
            self.cams_stages_b[stage]['camera'][camera] = status

    def get_camera_status(self):
        self.update_camera_status()
        return {"r": self.cams_stages_r, "b": self.cams_stages_b, "z": self.cams_stages_z}

    def get_qa_petals(self):
        return self.qa_petals
