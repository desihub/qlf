from __future__ import division
# Scalar_metrics.py DESISPEC 0.20.0
# To do: Finish the documentation

import logging
import requests
import os
import sys
from qlf_models import QLFModels
import json

logger = logging.getLogger(__name__)

desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')


class LoadMetrics:
    """ Read values from the json's files and return an alert (NORMAL, WARN or ALARM)
    associated to a given metric. It also attributes a color for a wedge in the interface
    CORRECTING WXSIGMA

    Functions:
    ----------     
        find_qa_check(qa)
        update_status(qa)
    """
    silent = 'False'  # Defining a silent mode
    prfx = 'ql-'
    qa_name = ['countpix', 'getbias', 'getrms', 'xwsigma',
               'countbins', 'integ', 'skycont', 'skypeak', 'skyresid', 'snr']

    def __init__(self, process_id, cam, exp=None, night=None):
        self.cam = cam
        self.exp = exp
        self.night = night
        self.process_id = process_id
        # This is True if the pipeline didn't generate some json file
        self.error = dict(zip(self.qa_name, ['False']*len(self.qa_name)))

        logger.info('check *rms_over *bias *SUMCOUNT_RMS shouldbe SUMCOUNT_MED_SKY'
                    + 'Resigf  skyresid- residrms')

        self.models = QLFModels()

        self.steps_list = ['preproc', 'extract', 'fiberfl', 'skysubs']

        self.steps_dic = {
            'preproc': ['countpix', 'getbias', 'getrms', 'xwsigma'],
            'extract': ['countbins'],
            'fiberfl': ['skycont', 'skypeak'],
            'skysubs': ['skyresid', 'integ', 'snr'],
        }

        self.alert_keys = {
            'getrms': 'NOISE_STATUS',
            'countpix': 'LITFRAC_STATUS',
            'getbias': 'BIAS_STATUS',
            'countbins': 'NGOODFIB_STATUS',
            'integ': 'DELTAMAG_STATUS',
            'xwsigma': 'XWSIGMA_STATUS',
            'snr': 'FIDSNR_STATUS',
            'skycont': 'SKYCONT_STATUS',
            'skypeak': 'PEAKCOUNT_STATUS',
            'skyresid': 'SKYRBAND_STATUS',
        }

        self.checks = {
            'CHECK_CCDs': ['getbias', 'countpix', 'getrms'],
            'CHECK_FIBERS': ['countbins', 'xwsigma'],
            'CHECK_SPECTRA': ['integ', 'snr', 'skypeak', 'skycont', 'skyresid']
        }

        self.status = {
            'preproc': {'steps_status': ['None', 'None', 'None', 'None']},
            'extract': {'steps_status': ['None']},
            'fiberfl': {'steps_status': ['None', 'None']},
            'skysubs': {'steps_status': ['None', 'None', 'None']},
        }

    def find_qa_check(self, qa):
        for check in self.checks:
            if qa in self.checks[check]:
                return check
        return None

    def load_merged_qa(self):
        data = None
        if self.process_id is not None:
            data = self.models.get_output(self.process_id, self.cam)
        return data

    def update_status(self, qa):
        index = -1
        current_step = None
        qa_status = None
        for step in self.steps_list:
            try:
                index = self.steps_dic[step].index(qa)
                current_step = step
                break
            except ValueError:
                continue

        data = self.load_merged_qa()
        try:
            alert_key = self.alert_keys[qa]
            check = self.find_qa_check(qa)
            qa_status = data["TASKS"][check]["METRICS"][alert_key]

            if current_step:
                self.status[current_step]['steps_status'][index] = qa_status
        except Exception as err:
            logger.warning('Failed to update camera status: {}'.format(err))

    def get_merged_qa_status(self):
        for qa in self.alert_keys.keys():
            self.update_status(qa)


if __name__ == "__main__":
    lm = LoadMetrics(39, 'b0', '3905', '20191017')
    # lm.update_status('snr')
    lm.get_merged_qa_status()
    print(lm.status)
