import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter

from dashboard.bokeh.helper import write_info

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import (LinearColorMapper ,    ColorBar)
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import Select
from dashboard.bokeh.qlf_plot import html_table, mtable, alert_table

from bokeh.io import output_notebook
import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description, get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import plot_hist

from bokeh.models import PrintfTickFormatter


import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)


class Integ:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)
        
        try:
            mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')

        gen_info = mergedqa['GENERAL_INFO']


        
        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
        std_fiberid = check_spectra['METRICS']['STAR_FIBERID']
        nrg = check_spectra['PARAMS']['DELTAMAG_TGT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['DELTAMAG_TGT_WARN_RANGE'] 
        fiber_mag=check_spectra['METRICS']['FIBER_MAG']


        hist_tooltip=""" 
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">INTEG: </span>
                    <span style="font-size: 13px; color: #515151;">@integ</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 13px; color: #515151;">@x</span>
                </div>
            </div>
                """
        hist_hover = HoverTool(tooltips=hist_tooltip)
        hist_source = ColumnDataSource(
                        data={'integ': fiber_mag,
                            'x': np.arange(len(fiber_mag)),
                            })

        yrange=[0, 1.1*max(fiber_mag)]
        fiber_hist = plot_hist(hist_hover, yrange, ph=300)

        fiber_hist.vbar(top='integ', x='x', width=0.8,
                    source=hist_source,
                    fill_color="dodgerblue", line_color="black", line_width =0.01, alpha=0.8,
                    hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
        fiber_hist.xaxis.axis_label="Fibers"
        fiber_hist.yaxis.axis_label="Integral (counts)"

        info_col=Div(text=write_description('integ'), width=fiber_hist.plot_width)

   

        #List of mag diff b/w the fibermag and the imaging mag from the fibermap
        tb = html_table(names=['DELTAMAG (Mean)'], vals=[ '{:.3f}'.format(np.mean(fiber_mag) )]
            , nrng=nrg, wrng=wrg  )
        tbinfo=Div(text=tb, width=400)

       # Prepare tables
        comments='List of the average fiber mag for each of N target types in this camera'
        metric_txt=mtable('integ', mergedqa, comments)# objtype=['ELG','STAR'] )
        metric_tb=Div(text=metric_txt, width=450)
        alert_txt = alert_table(nrg,wrg)
        alert_tb = Div(text=alert_txt, width=450)


        layout = column(widgetbox(info_col, css_classes=["header"]),
                    column(widgetbox(metric_tb),widgetbox(alert_tb), css_classes=["table-ranges"]),
                        fiber_hist,
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "INTEG")
