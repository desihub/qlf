from bokeh.layouts import column

from bokeh.models.widgets import Div

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title

from qlf_models import QLFModels
from dashboard.bokeh.helper import get_palette

import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)



class Arc:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)

        check_arc = mergedqa['TASKS']['CHECK_ARC']

        nrg = check_arc['PARAMS']['CHECKARC_NORMAL_RANGE']
        wrg = check_arc['PARAMS']['CHECKARC_WARN_RANGE']



        info_col = Title().write_description('arc')

        # Prepare tables
        current_exposures = check_arc['METRICS']['CHECKARC']
        reference_exposures = check_arc['PARAMS']['CHECKARC_REF']
        keynames = ["CHECKARC" + " ( P%d)" % i for i in range(3)]
        metric = Table().reference_table(keynames, current_exposures, reference_exposures)
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "ARC")
