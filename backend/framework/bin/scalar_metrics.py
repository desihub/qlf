from __future__ import division

import logging
import requests
import os
import sys
from qlf_models import QLFModels
import json

logger = logging.getLogger(__name__)

desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
qlf_root = os.environ.get('QLF_ROOT')


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

    def __init__(self, process_id, cam, exp=None, night=None, flavor=None):
        self.cam = cam
        self.exp = exp
        self.night = night
        self.process_id = process_id
        # This is True if the pipeline didn't generate some json file
        self.error = dict(zip(self.qa_name, ['False']*len(self.qa_name)))

        logger.info('check *rms_over *bias *SUMCOUNT_RMS shouldbe SUMCOUNT_MED_SKY'
                    + 'Resigf  skyresid- residrms')

        self.models = QLFModels()

        stages = self.load_flavors()

        self.steps_dic = dict()
        self.qas_status = dict()
        self.alert_keys = dict()
        for step in self.flavor_stages[flavor]['step_list']:
            self.steps_dic[step['name']] = list()
            self.qas_status[step['name']] = list()
            for qa in step['qa_list']:
                self.steps_dic[step['name']].append(qa['name'])
                self.qas_status[step['name']].append('None')
                self.alert_keys[qa['name']] = qa['status_key']

    def load_flavors(self):
        flavors = ['science', 'arc', 'flat']
        self.flavor_stages = dict()
        for flavor in flavors:
            flavor_path = os.path.join(qlf_root, "framework", "ql_mapping", "{}.json".format(flavor))
            try:
                stages_json = open(flavor_path).read()
                self.flavor_stages[flavor] = json.loads(stages_json)
            except Exception as err:
                logger.error("flavor file not found {}".format(err))

    def find_qa_check(self, qa):
        for check in self.steps_dic:
            if qa in self.steps_dic[check]:
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
        for step in list(self.steps_dic):
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
                self.qas_status[current_step][index] = qa_status
        except Exception as err:
            logger.warning('Failed to update camera status: {}'.format(err))

    def get_merged_qa_status(self):
        for qa in list(self.alert_keys):
            self.update_status(qa)


if __name__ == "__main__":
    lm = LoadMetrics(6, 'b0', '3905', '20191017', 'science')
    lm.get_merged_qa_status()
