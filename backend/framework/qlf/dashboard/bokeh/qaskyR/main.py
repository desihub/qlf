from bokeh.layouts import column

from bokeh.models.widgets import Div

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title

from qlf_models import QLFModels

import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)



class SkyR:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        gen_info = mergedqa['GENERAL_INFO']

        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']

        nrg = check_spectra['PARAMS']['SKYRBAND_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['SKYRBAND_WARN_RANGE']

        info_col = Title().write_description('skyR')

        # Prepare Tables
        current_exposures = [check_spectra['METRICS']['SKYRBAND']]
        program = gen_info['PROGRAM'].upper()
        reference_exposures = check_spectra['PARAMS']['SKYRBAND_' +
                                                      program + '_REF']
        keynames = ["SKYRBAND" for i in range(len(current_exposures))]
        table = Table().single_table(keynames, current_exposures, reference_exposures, nrg, wrg)

        layout = column(info_col, Div(),
                        table, Div(),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "SKYR")
