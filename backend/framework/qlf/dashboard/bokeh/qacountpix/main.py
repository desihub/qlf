from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox

from bokeh.models.widgets import PreText, Div
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.models import LinearColorMapper, ColorBar

import numpy as np

from dashboard.bokeh.helper import write_description, write_info, \
    get_merged_qa_scalar_metrics

from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import alert_table, mtable, \
    set_amp, plot_amp
import numpy as np
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

        cmap = get_palette("RdBu_r")


        name = 'LITFRAC_AMP'

        dz = countpix["LITFRAC_AMP"]

        mapper = LinearColorMapper(palette=cmap, low=wrg[0], high=wrg[1],
            nan_color="darkgray")


        dzdiff = np.array(dz)-np.array(refexp)

        ztext, cbarformat = set_amp(dz)
        p = plot_amp(dz, refexp, mapper, name=name)

        p.xaxis.axis_label = "Fraction over 5 sigma read noise (per Amp)"

        formatter = PrintfTickFormatter(format=cbarformat)
        color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                             major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                             formatter=formatter, title="(Val-Ref)", title_standoff=15,
                             title_text_baseline="alphabetic",)
        p.add_layout(color_bar, 'right')



        # infos
        info, nlines = write_info('countpix', tests)
        txt = PreText(text=info, height=nlines*20, width=2*p.plot_width)



        info_col = Div(text=write_description('countpix'))

        # Prepare tables
        metricname = 'LITFRAC_AMP'
        keyname = 'countpix'
        curexp = mergedqa['TASKS']['CHECK_CCDs']['METRICS']['LITFRAC_AMP']
        metric_txt = mtable('countpix', mergedqa)

        metric_tb = Div(text=metric_txt)

        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        column(p, sizing_mode='scale_both',
                               css_classes=["main-one"]),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "Countpix")
