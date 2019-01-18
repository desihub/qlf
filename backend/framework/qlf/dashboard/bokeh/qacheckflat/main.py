from bokeh.layouts import column

from bokeh.models.widgets import Div
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.models import LinearColorMapper, ColorBar

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title

from qlf_models import QLFModels
from dashboard.bokeh.helper import get_palette

import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)



class Flat:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        check_flat = mergedqa['TASKS']['CHECK_FIBERFLAT']
        flat = check_flat['METRICS']

        nrg = check_flat['PARAMS']['CHECKFLAT_NORMAL_RANGE']
        wrg = check_flat['PARAMS']['CHECKFLAT_WARN_RANGE']

        info_col = Title().write_description('fiberflat')

        # Prepare tables
        current_exposures = check_flat['METRICS']['CHECKFLAT']
        reference_exposures = check_flat['PARAMS']['CHECKFLAT_REF']
        keynames = ["CHECKFLAT"]
        metric = Table().reference_table(keynames, [current_exposures], reference_exposures)
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "FIBERFLAT")
