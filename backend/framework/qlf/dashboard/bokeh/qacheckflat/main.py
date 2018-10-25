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



class Flat:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        check_flat = mergedqa['TASKS']['CHECK_FIBERFLAT']
        flat = check_flat['METRICS']

        nrg = check_flat['PARAMS']['CHECKFLAT_NORMAL_RANGE']
        wrg = check_flat['PARAMS']['CHECKFLAT_WARN_RANGE']
        refexp = check_flat['PARAMS']['CHECKFLAT_REF']


        #info, nlines = write_info('getrms', check_ccds['PARAMS'])
        info = """<div> 
        <body><p  style="text-align:left; color:#262626; font-size:20px;">
                    <b>Check Fiber Flat</b> <br> Examine fiber flat and test for
                     stability and consistency 
        </body></div>"""
        nlines = 2
        txt = Div(text=info, width=450)
        info_col = Div(text=write_description('fiberflat'))


        # Prepare tables
        metric_txt = mtable('fiberflat', mergedqa)
        metric_tb = Div(text=metric_txt)

        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        # column(p, sizing_mode='scale_both'),
                        # column(p2, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "FIBERFLAT")
