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


class Countpix:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)

        countpix = mergedqa['TASKS']['CHECK_CCDs']['METRICS']
        tests = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']

        nrg = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP_NORMAL_RANGE']
        wrg = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP_WARN_RANGE']
        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        refexp = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP' +
                                                           program_prefix+'_REF']

        # PATCH
        p = Patch().plot_amp(
            dz=countpix["LITFRAC_AMP"],
            refexp=refexp,
            name="LITFRAC_AMP",
            description="Average bias value per Amp (photon counts)",
            wrg=wrg
        )

        # infos
        info_col = Title().write_description('countpix')

        # Prepare tables
        metric = Table().mtable('countpix', mergedqa)
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        column(p, sizing_mode='scale_both',
                               css_classes=["main-one"]),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "Countpix")
