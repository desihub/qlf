from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox

from bokeh.models.widgets import Div

from bokeh.models import HoverTool, ColumnDataSource
from dashboard.bokeh.qlf_plot import mtable, alert_table

import numpy as np

from dashboard.bokeh.helper import write_description, get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import plot_hist

import logging
from bokeh.resources import CDN
from bokeh.embed import file_html

import os

spectro_data = os.environ.get('DESI_SPECTRO_DATA')

logger = logging.getLogger(__name__)


class Integ:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(
            self.selected_process_id, cam)

        gen_info = mergedqa['GENERAL_INFO']

        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
        std_fiberid = check_spectra['METRICS']['STAR_FIBERID']
        nrg = check_spectra['PARAMS']['DELTAMAG_TGT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['DELTAMAG_TGT_WARN_RANGE']
        fiber_mag = check_spectra['METRICS']['FIBER_MAG']

        hist_tooltip = """ 
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">INTEG: </span>
                    <span style="font-size: 1vw; color: #515151;">@integ</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@x</span>
                </div>
            </div>
                """
        hist_hover = HoverTool(tooltips=hist_tooltip)
        hist_source = ColumnDataSource(
            data={'integ': fiber_mag,
                  'x': np.arange(len(fiber_mag)),
                  })

        yrange = [0, 1.1*max(fiber_mag)]
        fiber_hist = plot_hist(hist_hover, yrange, ph=350)

        fiber_hist.vbar(top='integ', x='x', width=0.8,
                        source=hist_source,
                        fill_color="dodgerblue", line_color="black", line_width=0.01, alpha=0.8,
                        hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
        fiber_hist.xaxis.axis_label = "Fibers"
        fiber_hist.yaxis.axis_label = "Integral (counts)"

        info_col = Div(text=write_description('integ'))

        # Reading obj_type
        try:
            from dashboard.models import Job, Process

            process_id = self.selected_process_id
            process = Process.objects.get(pk=process_id)
            joblist = [entry.camera.camera for entry in Job.objects.filter(
                process_id=process_id)]
            exposure = process.exposure
            fmap = Fibermap.objects.filter(exposure=exposure)
            otype_tile = fmap.objtype

            objlist = sorted(set(otype_tile))
            if 'SKY' in objlist:
                objlist.remove('SKY')

        except Exception as err:
            objlist = None

        # Prepare tables
        # objtype=['ELG','STAR'] )

        metric_txt = mtable('integ', mergedqa ,objtype=objlist)
        metric_tb = Div(text=metric_txt)
        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        font_size = "1vw"
        for plot in [fiber_hist]:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb, css_classes=["table-ranges"]),
                        widgetbox(alert_tb, css_classes=["table-ranges-sec"]),
                        column(fiber_hist, sizing_mode='scale_both', css_classes=["main-one"]),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "INTEG")
