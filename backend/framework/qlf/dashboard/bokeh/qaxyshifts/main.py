from bokeh.layouts import column

from bokeh.models.widgets import Div

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title

from dashboard.bokeh.helper import get_merged_qa_scalar_metrics

from bokeh.resources import CDN
from bokeh.embed import file_html


class Xyshifts:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)

        xyshifts = mergedqa['TASKS']['CHECK_FIBERS']

        nrg = xyshifts['PARAMS']['XYSHIFTS_NORMAL_RANGE']
        wrg = xyshifts['PARAMS']['XYSHIFTS_WARN_RANGE']

        info_col = Title().write_description('xyshifts')

        # Prepare tables
        metric = Table().mtable('xyshifts', mergedqa)
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "XYSHIFTS")
