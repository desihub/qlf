import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter

from dashboard.bokeh.helper import write_info, get_scalar_metrics

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import (LinearColorMapper ,    ColorBar)
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import Select
from dashboard.bokeh.qlf_plot import html_table

from bokeh.io import output_notebook
import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description
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
            lm = get_scalar_metrics(self.selected_process_id, cam)
            metrics, tests  = lm['metrics'], lm['tests']
        except:
            sys.exit('Could not load metrics')


        integ=metrics['integ']
        std_fiberid = integ['STD_FIBERID']
        #std_mag = np.where()


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
                        data={'integ': integ['FIBER_MAG'],
                            'x': np.arange(len(integ['FIBER_MAG'])),
                            #'left': np.arange(len(skyresid['SKYFIBERID'])) -0.4,
                            #'right':np.arange(len(skyresid['SKYFIBERID']))+0.4,
                            #'bottom':[0]*len(skyresid['SKYFIBERID']),
                            })

        yrange=[0, 1.1*max(integ['FIBER_MAG'])]
        fiber_hist = plot_hist(hist_hover, yrange, ph=300)

        fiber_hist.vbar(top='integ', x='x', width=0.8,
                    source=hist_source,
                    fill_color="dodgerblue", line_color="black", line_width =0.01, alpha=0.8,
                    hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
        fiber_hist.xaxis.axis_label="Fibers"
        fiber_hist.yaxis.axis_label="Integral (counts)"

        info_col=Div(text=write_description('integ'), width=fiber_hist.plot_width)

        nrg= tests['integ']['DELTAMAG_WARN_RANGE']
        wrg= tests['integ']['DELTAMAG_NORMAL_RANGE']

        #List of mag diff b/w the fibermag and the imaging mag from the fibermap
        tb = html_table(names=['DELTAMAG (Mean)'], vals=[ '{:.3f}'.format(np.mean(integ['DELTAMAG']) )], nrng=nrg, wrng=wrg  )
        tbinfo=Div(text=tb, width=400)

        layout = column(widgetbox(info_col, css_classes=["header"]),
                        widgetbox(tbinfo, css_classes=["table-ranges"]),
                        fiber_hist,
                        css_classes=["display-grid"])
        # End of Bokeh Block
        return file_html(layout, CDN, "INTEG")
