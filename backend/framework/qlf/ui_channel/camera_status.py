import os
import configparser
import copy
import logging

logger = logging.getLogger(__name__)

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

try:
    cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
except Exception as error:
    logger.error(error)
    logger.error("Error reading  %s/framework/config/qlf.cfg" % qlf_root)


class CameraStatus:
    def __init__(self):
        self.reset_camera_status()

    def reset_camera_status(self):
        self.cams_stages_r = list()
        for i in range(4):
            self.cams_stages_r.append(
                    dict(camera=[i for i in range(10)])
            )

            self.cams_stages_b = copy.deepcopy(self.cams_stages_r)
            self.cams_stages_z = copy.deepcopy(self.cams_stages_r)

        self.qa_petals = list()

    def update_qa_state(self, camera, cam, log):
        for line in log:
            if 'BIAS_STATUS' in line:
                camera[cam]['preproc']['steps_status'][1] = line.split(
                    'BIAS_STATUS:'
                )[1][1:-1]
            elif 'XWSIGMA_STATUS' in line:
                camera[cam]['preproc']['steps_status'][3] = line.split(
                    'XWSIGMA_STATUS:'
                )[1][1:-1]
            elif 'LITFRAC_STATUS' in line:
                camera[cam]['preproc']['steps_status'][0] = line.split(
                    'LITFRAC_STATUS:'
                )[1][1:-1]
            elif 'NOISE_STATUS' in line:
                camera[cam]['preproc']['steps_status'][2] = line.split(
                    'NOISE_STATUS:'
                )[1][1:-1]
            elif 'NGOODFIB_STATUS' in line:
                camera[cam]['extract']['steps_status'][0] = line.split(
                    'NGOODFIB_STATUS:'
                )[1][1:-1]
            elif 'SKYCONT_STATUS' in line:
                camera[cam]['fiberfl']['steps_status'][0] = line.split(
                    'SKYCONT_STATUS:'
                )[1][1:-1]
            elif 'PEAKCOUNT_STATUS' in line:
                camera[cam]['fiberfl']['steps_status'][1] = line.split(
                    'PEAKCOUNT_STATUS:'
                )[1][1:-1]
            elif 'FIDSNR_STATUS' in line:
                camera[cam]['skysubs']['steps_status'][2] = line.split(
                    'FIDSNR_STATUS:'
                )[1][1:-1]
            elif 'DELTAMAG_STATUS' in line:
                camera[cam]['skysubs']['steps_status'][0] = line.split(
                    'DELTAMAG_STATUS:'
                )[1][1:-1]
            elif 'RESID_STATUS' in line:
                camera[cam]['skysubs']['steps_status'][1] = line.split(
                    'RESID_STATUS:'
                )[1][1:-1]

    def update_petals(self, cam, log):
        cam_index = None

        for index, qa_petal in enumerate(self.qa_petals):
            if cam in qa_petal.keys():
                cam_index = index

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
            self.update_qa_state(camera, cam, log)
            self.qa_petals.append(camera)
        else:
            camera = self.qa_petals[cam_index]
            self.update_qa_state(camera, cam, log)
            self.qa_petals[cam_index] = camera

    def update_camera_status(self, process):
        label_name = list()

        for num in range(30):
            if 'z9' not in label_name:
                label_name.append('z' + str(num))
            elif 'r9' not in label_name:
                label_name.append('r' + str(num - 10))
            elif 'b9' not in label_name:
                label_name.append('b' + str(num - 20))

            for cam in label_name:
                cameralog = None
                log = str()
                try:
                    for item in process.get("process_jobs", list()):
                        if cam == item.get("camera"):
                            cameralog = os.path.join(
                                desi_spectro_redux,
                                item.get('logname')
                            )
                            break
                    if cameralog:
                        arq = open(cameralog, 'r')
                        log = arq.readlines()
                        if log:
                            self.update_petals(cam, log)

                except Exception as e:
                    logger.warn(e)

                if "Pipeline completed. Final result" in ''.join(log):
                    self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 1, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 2, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 3, int(cam[1:]), 'success_stage')
                elif "Starting to run step SkySub_QL" in ''.join(log):
                    self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 1, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 2, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 3, int(cam[1:]), 'processing_stage')
                    next

                elif "Starting to run step ApplyFiberFlat_QL" in ''.join(log):
                    self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 2, int(cam[1:]), 'processing_stage')
                    self.update_stage(cam[:1], 1, int(cam[1:]), 'success_stage')
                    next

                elif "Starting to run step BoxcarExtract" in ''.join(log):
                    self.update_stage(cam[:1], 0, int(cam[1:]), 'success_stage')
                    self.update_stage(cam[:1], 1, int(cam[1:]), 'processing_stage')
                    next

                elif "Starting to run step Preproc" in ''.join(log):
                    self.update_stage(cam[:1], 0, int(cam[1:]), 'processing_stage')
                    next
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

    def get_camera_status(self, process):
        self.update_camera_status(process)
        return {"r": self.cams_stages_r, "b": self.cams_stages_b, "z": self.cams_stages_z}

    def get_qa_petals(self):
        return self.qa_petals
