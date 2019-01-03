from bokeh.layouts import column

from bokeh.models.widgets import Div

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.patch.main import Patch

from dashboard.bokeh.helper import get_merged_qa_scalar_metrics

import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)


class RMS:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        check_ccds = mergedqa['TASKS']['CHECK_CCDs']
        getrms = check_ccds['METRICS']

        nrg = check_ccds['PARAMS']['NOISE_AMP_NORMAL_RANGE']
        wrg = check_ccds['PARAMS']['NOISE_AMP_WARN_RANGE']
        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        refexp = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['NOISE_AMP' +
                                                           program_prefix+'_REF']

        # amp 1
        p = Patch().plot_amp(
            dz=getrms["NOISE_AMP"],
            refexp=refexp,
            name="NOISE_AMP",
            description="NOISE per Amp (photon counts)",
            wrg=wrg
        )

        # amp 2
        p2 = Patch().plot_amp(
            dz=getrms["NOISE_OVERSCAN_AMP"],
            refexp=refexp,
            name="NOISE_OVERSCAN_AMP",
            description="NOISE Overscan per Amp (photon counts)",
            wrg=wrg
        )

        info_col = Title().write_description('getrms')

        # Prepare tables
        metric = Table().mtable('getrms', mergedqa, )
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        column(p, sizing_mode='scale_both'),
                        column(p2, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "GETRMS")
