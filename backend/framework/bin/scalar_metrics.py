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
        Load_qa(qa)
        Load_metrics_n_tests()
        step_status(step_name)
        get_qa_step_color(step)
        load_qa_tests()
    """
    silent = 'False'  # Defining a silent mode
    prfx = 'ql-'
    
    #SE: this includes all the changes in qa_names for science processing 
    qa_name = ['checkHDUs','countpix', 'getbias', 'getrms', 'trace', 'xwsigma',
               'countbins', 'integ', 'skycont', 'skypeak', 'skyRband', 'snr']
    
    #SE: replace qa_name with the one below if it is OK to add the qa_names that are specific to ARC and FLAT exposures
    
    #qa_name = ['checkHDUs','countpix', 'getbias', 'getrms', 'trace', 'xwsigma',
    #           'countbins', 'integ', 'skycont', 'skypeak', 'skyRband', 'snr', 'checkfibflat', 'checkres']
    
     
    def __init__(self, process_id, cam, exp=None, night=None):
        self.cam = cam
        self.exp = exp
        self.night = night
        self.process_id = process_id
        # This is True if the pipeline didn't generate some json file
        self.error = dict(zip(self.qa_name, ['False']*len(self.qa_name)))

        self.models = QLFModels()

        self.steps_list = ['preproc', 'flexure', 'extract', 'fiberfl', 'skysubs']

         
        self.steps_dic = {
            'preproc': ['checkHDUs', 'countpix', 'getbias', 'getrms', 'xwsigma'],
            'flexure': ['trace'],
            'extract': ['countbins'],
            'fiberfl': ['skycont', 'skypeak'],
            'skysubs': ['skyRband','integ', 'snr'],
        }
        
        self.alert_keys = {
            'checkHDUs': 'CHECKHDUS_STATUS',
            'getrms': 'NOISE_AMP_STATUS',
            'countpix': 'LITFRAC_AMP_STATUS',
            'getbias': 'BIAS_AMP_STATUS',
            'countbins': 'NGOODFIB_STATUS',
            'xwsigma': 'XWSIGMA_STATUS',
            'trace': 'XYSHIFTS_STATUS',
            'skycont': 'SKYCONT_STATUS',
            'skypeak': 'PEAKCOUNT_STATUS',
            'skyRband': 'SKYRBAND_STATUS',
            'integ': 'DELTAMAG_TGT_STATUS',
            'snr': 'FIDSNR_TGT_STATUS',
        }
        
           

        self.checks = {
            'CHECK_CCDs': ['checkHDUs', 'getbias', 'countpix', 'getrms'],
            'CHECK_FIBERS': ['countbins','trace', 'xwsigma'],
            'CHECK_SPECTRA': ['skypeak', 'skycont', 'skyRband', 'integ', 'snr']
        }

        self.status = {
            'preproc': {'steps_status': ['None', 'None','None', 'None', 'None']},
            'extract': {'steps_status': ['None']},
            'flexure': {'steps_status': ['None']},
            'fiberfl': {'steps_status': ['None', 'None']},
            'skysubs': {'steps_status': ['None', 'None', 'None']},
        }
        
        # SE: A proposal in case QLF is flavour agnostic-  Replace this section with lines 53-93 if it is OK to add flavour-specific steps and scalar metrics to the list 

            
        """
        self.steps_list = ['preproc', 'flexure', 'extract', 'compute_fibflat', 'resfit', 'fiberfl', 'skysubs']
         
        self.steps_dic = {
            'preproc': ['checkHDUs', 'countpix', 'getbias', 'getrms', 'xwsigma'],
            'flexure': ['trace'],
            'extract': ['countbins'],
            'compute_fibflat' : ['checkfibflat'],
            'resfit': ['checkres'],
            'fiberfl': ['skycont', 'skypeak'],
            'skysubs': ['skyRband','integ', 'snr'],
        }
        
        self.alert_keys = {
            'checkHDUs': 'CHECKHDUS_STATUS',
            'getrms': 'NOISE_AMP_STATUS',
            'countpix': 'LITFRAC_AMP_STATUS',
            'getbias': 'BIAS_AMP_STATUS',
            'countbins': 'NGOODFIB_STATUS',
            'xwsigma': 'XWSIGMA_STATUS',
            'trace': 'XYSHIFTS_STATUS',
            'skycont': 'SKYCONT_STATUS',
            'skypeak': 'PEAKCOUNT_STATUS',
            'skyRband': 'SKYRBAND_STATUS',
            'integ': 'DELTAMAG_TGT_STATUS',
            'snr': 'FIDSNR_TGT_STATUS',
            'checkfibflat': 'CHECKFLAT_STATUS',
            'checkres' : 'CHECKARC_STATUS',
        }
        
           

        self.checks = {
            'CHECK_CCDs': ['checkHDUs', 'getbias', 'countpix', 'getrms'],
            'CHECK_FIBERS': ['countbins','trace', 'xwsigma','checkfibflat','checkres'],
            'CHECK_SPECTRA': ['skypeak', 'skycont', 'skyRband', 'integ', 'snr']
        }

        self.status = {
            'preproc': {'steps_status': ['None', 'None','None', 'None', 'None']},
            'extract': {'steps_status': ['None']},
            'flexure': {'steps_status': ['None']},
            'compute_fibflat' : {'steps_status': ['None']},
            'resfit': {'steps_status': ['None']},
            'fiberfl': {'steps_status': ['None', 'None']},
            'skysubs': {'steps_status': ['None', 'None', 'None']},
        }


        """
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

    def load_output(self):
        """ Returns a json with the camera output per job """

        cam, process_id = self.cam, self.process_id
        return self.models.get_output(process_id, cam)

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
            flexure = self.get_qa_step_color('flexure')
            extract = self.get_qa_step_color('extract')
            # SE: uncomment the next two lines if decided to uncommnet lines 99-144
            #compute_fibflat = self.get_qa_step_color('compute_fibflat')
            #resfit =  self.get_qa_step_color('resfit')
            fiberfl = self.get_qa_step_color('fiberfl')
            skysubs = self.get_qa_step_color('skysubs')
            qa_tests = {'preproc': preproc, 'flexure': flexure, 'extract': extract,
                        'fiberfl': fiberfl, 'skysubs': skysubs}
            # SE: uncomment the next line if decided to uncommnet lines 99-144
            #qa_tests = {'preproc': preproc, 'flexure': flexure, 'extract': extract, 'compute_fibflat': compute_fibflat, 'resfit':resfit,
            #            'fiberfl': fiberfl, 'skysubs': skysubs}
            
            return qa_tests
        except:
            logger.error('Camera not found %s' % (self.cam))

    def load_merged_qa(self):
        cam, exp, night, process_id = self.cam, \
                                      self.exp, \
                                      self.night, \
                                      self.process_id

        data = None

        if process_id is not None:
            data = self.models.get_merged_qa(process_id, cam)

        return data

    def find_qa_check(self, qa):
        for check in self.checks:
            if qa in self.checks[check]:
                return check
        return None

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
    # lm.update_status('countpix')
    # lm.update_status('getrms')
    # lm.update_status('xwsigma')
    # lm.update_status('snr')
    lm.get_merged_qa_status()
    print(lm.status)
