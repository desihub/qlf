from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox

from bokeh.models.widgets import PreText, Div
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.models import LinearColorMapper, ColorBar

import numpy as np

from dashboard.bokeh.helper import write_description, write_info,\
                     get_merged_qa_scalar_metrics, get_palette
from dashboard.bokeh.qlf_plot import alert_table,\
    mtable, set_amp, plot_amp

import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)


class Bias:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        check_ccds = mergedqa['TASKS']['CHECK_CCDs']
        getbias = check_ccds['METRICS']

        nrg = check_ccds['PARAMS']['BIAS_AMP_NORMAL_RANGE']
        wrg = check_ccds['PARAMS']['BIAS_AMP_WARN_RANGE']
        tests = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']
        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        refexp = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['BIAS_AMP' +
                                                           program_prefix+'_REF']


        # amp
        name = 'BIAS_AMP'
        metr = getbias

        dz = getbias[name]  

        cmap = get_palette("RdBu_r")
        mapper = LinearColorMapper(palette=cmap, low=wrg[0], high=wrg[1],
            nan_color="darkgrey")

        ztext, cbarformat = set_amp(getbias["BIAS_AMP"])
        p = plot_amp(dz,refexp, mapper, name = name)

        p.xaxis.axis_label= "Average bias value per Amp (photon counts)"

        formatter = PrintfTickFormatter(format=cbarformat)
        color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                             major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                             formatter=formatter, title="(Val-Ref)", title_standoff=15,
                              title_text_baseline="alphabetic")
        p.add_layout(color_bar, 'right')

        # INFO TABLES:
        info, nlines = write_info('getbias', tests)
        try:
            info_hist = """
            <p style="font-size:1vw;"> BIAS: {} </p>
            """.format(getbias['BIAS'])
        except:
            info_hist = """"""
        txt = Div(text=info_hist)

        info_col = Div(text=write_description('getbias'))

        # Prepare tables
        metricname='BIAS_AMP'
        keyname='getbias'
        metric_txt=mtable('getbias', mergedqa)
        metric_tb=Div(text=metric_txt)

        alert_txt = alert_table(nrg,wrg)
        alert_tb = Div(text=alert_txt)
        p.sizing_mode = "scale_width"


        ptxt = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb),widgetbox(alert_tb),
                        column(p, sizing_mode='scale_both', css_classes=["main-one"]),
                        css_classes=["display-grid"])


        return file_html(ptxt, CDN, "GETBIAS")
