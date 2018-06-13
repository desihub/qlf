from __future__ import division
# Scalar_metrics.py DESISPEC 0.20.0
# To do: Finish the documentation

import logging
import requests
import os
import sys
from qlf_models import QLFModels
import json
from util import get_config

logger = logging.getLogger(__name__)

cfg = get_config()
desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')


class LoadMetrics:
    """ Read values from the json's files and return an alert (NORMAL, WARN or ALARM)
    associated to a given metric. It also attributes a color for a wedge in the interface
    CORRECTING WXSIGMA

    Functions:
    ----------     
        Load_qa(qa)
        Load_metrics_n_tests()
        step_status(step_name)
        get_qa_step_color(step)
        load_qa_tests()
    """
    silent = 'False'  # Defining a silent mode
    prfx = 'ql-'
    qa_name = ['countpix', 'getbias', 'getrms', 'xwsigma',
               'countbins', 'integ', 'skycont', 'skypeak', 'skyresid', 'snr']

    def __init__(self, process_id, cam, exp, night):
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
            'fiberfl': ['integ', 'skycont', 'skypeak'],
            'skysubs': ['skyresid', 'integ', 'snr'],
        }

        self.alert_keys = {
            'getrms': 'NOISE_STATUS',
            'countpix': 'NPIX_STATUS',
            'getbias': 'BIAS_STATUS',
            'countbins': 'NGOODFIB_STATUS',
            'integ': 'DELTAMAG_STATUS',
            'xwsigma': 'XWSIGMA_STATUS',
            'snr': 'FIDSNR_STAT',
            'skycont': 'SKYCONT_STATUS',
            'skypeak': 'PEAKCOUNT_STATUS',
            'skyresid': 'RESIDRMS_STAT',
        }

        self.status = {
            'extract': {'steps_status': ['None']},
            'preproc': {'steps_status': ['None', 'None', 'None', 'None']},
            'fiberfl': {'steps_status': ['None', 'None']},
            'skysubs': {'steps_status': ['None', 'None', 'None']},
        }

    def Load_qa(self, qa):
        """loads a single json file ( rather slow!)

        Arguments
        ---------
        qa --
        cam --
        exp --
        night --
        Return
        ------
        y2: list
        """

        cam, exp, night, process_id = self.cam, self.exp, self.night, self.process_id

        exp_zfill = str(exp).zfill(8)
        qa_name = '{}{}-{}-{}.json'.format(self.prfx, qa, cam, exp_zfill)
        data = None
        if process_id is not None:
            data = self.models.get_qa(process_id, cam, qa_name)
        else:
            qa_file_path = "{}/exposures/{}/{}/{}".format(desi_spectro_redux, night, exp_zfill, qa_name)
            try:
                if os.path.exists(qa_file_path):
                    with open(qa_file_path) as f:
                        data = json.load(f)
            except Exception as e:
                data = None
                logger.error("Could not open {}".format(qa_name))

        if data:
            self.error.update({qa: False})
        else:
            self.error.update({qa: True})

        return data

    def Load_metrics_n_tests(self):
        """ Gathers all the json info in 'METRICS' and 'PARAMS'
        and returns them in individual dictionaries
        Uses: Load_qa

        Arguments
        ---------
        qa_name: lst or str
            A name or list of names of qa's

        Return
        ------
        dic_met: dictionary
            A dictionary with the metric values 

        dic_test: dictionary
            A dictionary with the test values

        """
        dic_met = {}
        dic_tst = {}

        if isinstance(self.qa_name, list):
            qa_list = self.qa_name
        elif isinstance(self.qa_name, str):  # for a single qa_name
            qa_list = [self.qa_name]
        else:
            return "Invalid QA format"
        for i in qa_list:
            try:
                aux = self.Load_qa(i)
                if aux == None:
                    dic_met.update({i: aux})
                    dic_tst.update({i: aux})
                    self.error.update({i: True})
                else:
                    if self.process_id is not None:
                        dic_met.update({i: aux.metrics})
                        dic_tst.update({i: aux.params})
                    else:
                        dic_met.update({i: aux['METRICS']})
                        dic_tst.update({i: aux['PARAMS']})
            except Exception as e:  # ff
                print('------------->>>')
                print(e)

        return dic_met, dic_tst

    def step_status(self, step_name):
        """ Reading step color produced in desispec 0.20.0

        Arguments
        ---------
        step_name: str
            The abbreviated name of one of the four QA steps
        Return
        ------
        color: str
            Wedge color Alert
        """

        self.step_name = step_name
        if not isinstance(self.step_name, str):
            return "{} is not a String".format(self.step_name)
        if self.step_name not in self.steps_list:
            return "Invalid step: please return a value in {}".format(self.steps_list)

        # begin for desispec >= 0.17.1
        steps_status = []

        for i in self.steps_dic[self.step_name]:
            try:
                aux1 = self.metrics[i][self.alert_keys[i]]
            except Exception as e:
                # logger.error('Failed metric alert: '+ str(e)[:20])
                aux1 = 'None'

            steps_status.append(aux1)
        # end
        result = {'steps_status': steps_status}
        return result

    def get_qa_step_color(self, step):
        try:
            return self.step_status(step)
        except:
            return None

    def load_qa_tests(self):
        try:
            self.metrics, self.tests = self.Load_metrics_n_tests()
            preproc = self.get_qa_step_color('preproc')
            extract = self.get_qa_step_color('extract')
            fiberfl = self.get_qa_step_color('fiberfl')
            skysubs = self.get_qa_step_color('skysubs')
            qa_tests = {'preproc': preproc, 'extract': extract,
                        'fiberfl': fiberfl, 'skysubs': skysubs}
            return qa_tests
        except:
            logger.error('Camera not found %s' % (self.cam))

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

        data = self.Load_qa(qa)

        try:
            qa_status = data['METRICS'][self.alert_keys[qa]]

            if current_step:
                self.status[current_step]['steps_status'][index] = qa_status
        except Exception as err:
            logger.warning('Failed to update camera status: {}'.format(err))


if __name__ == "__main__":
    lm = LoadMetrics(None, 'z6', '00000062', '20180523')
    lm.update_status('countpix')
    print(lm.status)
