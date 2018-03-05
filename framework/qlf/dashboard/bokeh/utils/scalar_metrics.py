from __future__ import division
# Scalar_metrics.py DESISPEC 0.17.1
# To do: Finish the documentation

import logging
import requests
import os
import sys

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

logger = logging.getLogger(__name__)

class LoadMetrics:
    """ Read values from the yaml's files and return an alert (NORMAL, WARN or ALARM)
    associated to a given metric. It also attributes a color for a wedge in the interface 
    CORRECTING WXSIGMA

    Functions:
    ----------     
        Load_qa(qa)
        Load_metrics_n_tests()
    """
    silent = 'False' # Defining a silent mode
    prfx = 'ql-'
    qa_name    = ['countpix', 'getbias', 'getrms'
                   , 'xwsigma', 'countbins', 'integ'
                   , 'skycont', 'skypeak', 'skyresid', 'snr']
    
    params_keys = [['NPIX_ALARM_RANGE', 'CUTHI', 'NPIX_WARN_RANGE', 'CUTLO']
               , ['DIFF_ALARM_RANGE', 'PERCENTILES', 'DIFF_WARN_RANGE']
               , ['RMS_ALARM_RANGE', 'RMS_WARN_RANGE']
               , ['B_PEAKS', 'R_PEAKS', 'XSHIFT_ALARM_RANGE', 'WSHIFT_ALARM_RANGE'
                              , 'Z_PEAKS', 'WSHIFT_WARN_RANGE', 'XSHIFT_WARN_RANGE']
               , ['CUTHI', 'CUTLO', 'CUTMED', 'NGOOD_ALARM_RANGE', 'NGOOD_WARN_RANGE']
               , ['MAGDIFF_ALARM_RANGE', 'MAGDIFF_WARN_RANGE']
               , ['SKYCONT_ALARM_RANGE', 'SKYCONT_WARN_RANGE', 'B_CONT', 'Z_CONT', 'R_CONT']
               , ['B_PEAKS', 'R_PEAKS', 'SUMCOUNT_WARN_RANGE', 'SUMCOUNT_ALARM_RANGE', 'Z_PEAKS']
               , ['PCHI_RESID', 'PER_RESID', 'SKY_ALARM_RANGE', 'SKY_WARN_RANGE', 'BIN_SZ']
               , ['FIDSNR_WARN_RANGE', 'FIDSNR_ALARM_RANGE', 'FIDMAG']]
    
    params_dict = {'countbins': ['CUTHI', 'CUTLO', 'CUTMED', 'NGOOD_ALARM_RANGE', 'NGOOD_WARN_RANGE'],
                'countpix': ['NPIX_ALARM_RANGE', 'CUTHI', 'NPIX_WARN_RANGE', 'CUTLO'],
                'getbias': ['DIFF_ALARM_RANGE', 'PERCENTILES', 'DIFF_WARN_RANGE'],
                'getrms': ['RMS_ALARM_RANGE', 'RMS_WARN_RANGE'],
                'integ': ['MAGDIFF_ALARM_RANGE', 'MAGDIFF_WARN_RANGE'],
                'skycont': ['SKYCONT_ALARM_RANGE', 'SKYCONT_WARN_RANGE', 'B_CONT', 'Z_CONT', 'R_CONT'],
                'skypeak': ['B_PEAKS', 'R_PEAKS', 'SUMCOUNT_WARN_RANGE'
                             , 'SUMCOUNT_ALARM_RANGE',  'Z_PEAKS'],
                'skyresid': ['PCHI_RESID',  'PER_RESID', 'SKY_ALARM_RANGE', 'SKY_WARN_RANGE', 'BIN_SZ'],
                'snr': ['FIDSNR_WARN_RANGE', 'FIDSNR_ALARM_RANGE', 'FIDMAG'],
                'xwsigma':  ['B_PEAKS',  'R_PEAKS',  'XSHIFT_ALARM_RANGE', 'WSHIFT_ALARM_RANGE'
                             ,  'Z_PEAKS',  'WSHIFT_WARN_RANGE',  'XSHIFT_WARN_RANGE']}
    
 
    

    def __init__(self, cam,exp,night):
        self.cam   = cam
        self.exp   = exp
        self.night = night
        # This is True if the pipeline didn't generate some yaml file
        self.error = dict(zip(self.qa_name, ['False']*len(self.qa_name)) )
        
        logger.info('check *rms_over *bias *SUMCOUNT_RMS shouldbe SUMCOUNT_MED_SKY'
                 +'Resigf  skyresid- residrms')
        # QA tests and keys to respective values
        self.metric_qa_list  = ['getbias','getrms','skycont', 'countbins', 'countpix', 'snr'
                                ,'skyresid', 'skypeak',  'integ',  'xsigma', 'wsigma'   ] #THIS LINE : TB CHECKED
        self.metric_key_list = ['BIAS','RMS_OVER','SKYCONT','NGOODFIBERS', 'NPIX_LOW', 'ELG_FIDMAG_SNR'
                                ,'RESID_RMS', 'SUMCOUNT_MED_SKY', 'MAGDIFF_AVG', 'XSHIFT', 'WSHIFT']
        self.metric_dict     = dict(zip(self.metric_qa_list, self.metric_key_list))

        try: #ff
            self.metrics, self.tests = self.Load_metrics_n_tests()
        except: #ff
            sys.exit("Could not load metrics and tests" )

    def Load_qa(self, qa):
        """loads a single yaml file ( rather slow!)
         
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
        import yaml
        cam, exp, night = self.cam, self.exp, self.night

        exp_zfill = str(exp).zfill(8)
        qa_name = '{}{}-{}-{}.yaml'.format(self.prfx, qa, cam, exp_zfill)
        api = requests.get(QLF_API_URL).json()

        data = requests.get(api['qa'], params={'name': qa_name}).json()

        #print('qa',qa_name)
        #print('***', data['results'].keys() )
        if data['results'] == []:
            data = None
        else:
            data = data['results'][0]


        if data != None:
            self.error.update({qa:False})
        else:
            self.error.update({qa:True})
        return data

    
    def Load_metrics_n_tests(self):
        """ Gathers all the yaml info in 'METRICS' and 'PARAMS'
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
        elif isinstance(self.qa_name, string): # for a single qa_name
            qa_list = [self.qa_name]
        else:
            return "Invalid QA format"
            
        for i in qa_list:
            aux = self.Load_qa(i)
            if aux == None:
                dic_met.update({i: aux})
                dic_tst.update({i: aux})
                self.error.update({i:True})
            else:
                dic_met.update({i: aux['metrics']})
                dic_tst.update({i: aux['params']})
        return dic_met, dic_tst
