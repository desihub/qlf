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
        refexp = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['NOISE_AMP_REF']

        cmap = get_palette('RdBu_r')


        # amp 1
        dz = getrms['NOISE_AMP']
        name = 'NOISE_AMP'

        mapper = LinearColorMapper(palette=cmap, low=wrg[0], high=wrg[1],
            nan_color='darkgray')
        
        dzdiff = np.array(dz)-np.array(refexp)

        ztext, cbarformat = set_amp(dz)
        p = plot_amp(dz, refexp, mapper, name=name)

        p.xaxis.axis_label = "NOISE per Amp (photon counts)"

        formatter = PrintfTickFormatter(format=cbarformat)
        color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                             major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                             formatter=formatter, title="(Val-Ref)", title_standoff=15,
                             title_text_baseline="alphabetic",)
        p.add_layout(color_bar, 'right')



        # amp 2
        dz = getrms['NOISE_OVERSCAN_AMP']
        name = 'NOISE_OVERSCAN_AMP'

        mapper = LinearColorMapper(palette=cmap,  low=wrg[0], high=wrg[1],
            nan_color='darkgray')

        dzdiff = np.array(dz)-np.array(refexp)
        ztext, cbarformat = set_amp( dz)
        p2 = plot_amp(dz, refexp, mapper, name=name)

        p2.xaxis.axis_label = "NOISE Overscan per Amp (photon counts)"

        formatter = PrintfTickFormatter(format=cbarformat)
        color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                             major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                             formatter=formatter, title="(Val-Ref)", title_standoff=15,
                              title_text_baseline="alphabetic",)
        p2.add_layout(color_bar, 'right')

        info, nlines = write_info('getrms', check_ccds['PARAMS'])
        info = """<div> 
        <body><p  style="text-align:left; color:#262626; font-size:20px;">
                    <b>Get RMS</b> <br>Used to calculate RMS of region of 2D image, including overscan.</body></div>"""
        nlines = 2
        txt = Div(text=info, width=p.plot_width)
        info_col = Div(text=write_description('getrms'))


        # Prepare tables

        comments = 'value of RMS for each amplifier read directly from the header of the pre processed image'
        metric_txt = mtable('getrms', mergedqa)
        metric_tb = Div(text=metric_txt)

        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        column(p, sizing_mode='scale_both'),
                        column(p2, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "GETRMS")
