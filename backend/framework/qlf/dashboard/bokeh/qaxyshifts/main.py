from bokeh.layouts import column

from bokeh.models.widgets import Div

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title

from qlf_models import QLFModels

from bokeh.resources import CDN
from bokeh.embed import file_html


class Xyshifts:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)

        check_fibers = mergedqa['TASKS']['CHECK_FIBERS']
        gen_info = mergedqa['GENERAL_INFO']
        flavor = mergedqa['FLAVOR']

        nrg = check_fibers['PARAMS']['XYSHIFTS_NORMAL_RANGE']
        wrg = check_fibers['PARAMS']['XYSHIFTS_WARN_RANGE']

        info_col = Title().write_description('xyshifts')

        # Prepare tables
        current_exposures = check_fibers['METRICS']['XYSHIFTS']
        program = gen_info['PROGRAM'].upper()
        if flavor == 'science':
            reference_exposures = check_fibers['PARAMS']['XYSHIFTS_' +
                                                        program + '_REF']
        else:
            reference_exposures = []
        keynames = ["X", "Y"]
        table = Table().single_table(keynames, current_exposures, reference_exposures, nrg, wrg)

        layout = column(info_col, Div(),
                        table, Div(),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "XYSHIFTS")
