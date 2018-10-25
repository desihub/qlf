from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox

from bokeh.models.widgets import Div
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.models import LinearColorMapper, ColorBar

from dashboard.bokeh.qlf_plot import mtable, alert_table

import numpy as np

from dashboard.bokeh.helper import write_description, write_info,\
    get_merged_qa_scalar_metrics
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import set_amp, plot_amp

import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)



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

        info_col = Div(text=write_description('xyshifts'))

        # Prepare tables
        metric_txt = mtable('xyshifts', mergedqa)
        metric_tb = Div(text=metric_txt)

        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "XYSHIFTS")
