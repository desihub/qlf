import sys

from bokeh.plotting import figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models.widgets import PreText
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.helper import write_info


from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import ColumnDataSource, HoverTool, TapTool, Range1d, OpenURL
from bokeh.models import LinearColorMapper , ColorBar
from bokeh.models.widgets import Select, Slider
from dashboard.bokeh.helper import get_url_args

import numpy as np
import logging

logger = logging.getLogger(__name__)

# =============================================
# THIS comes from INTERFACE
#
args = get_url_args(curdoc)

try:
    selected_exposure = args['exposure']
    selected_arm = args['arm']
    selected_spectrograph = args['spectrograph']
except:
    sys.exit('Invalid args')

# =============================================
# THIS comes from QLF.CFG
#
night = '20190101'

# ============================================
#  THIS READ yaml files
#
from dashboard.bokeh.utils.scalar_metrics import LoadMetrics

cam = selected_arm+str(selected_spectrograph)
exp = selected_exposure # intentionaly redundant
lm = LoadMetrics(cam, exp, night);
metrics, tests  = lm.metrics, lm.tests 

skyresid  = metrics['skyresid']

# ============================================
# THIS: Given the set up in the block above, 
#       we have the bokeh plots

skr_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
            <span style="font-size: 13px; color: #515151">@wl &#8491</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
            <span style="font-size: 13px; color: #515151;">@med_resid</span>
        </div>
    </div>
"""

wavg_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
            <span style="font-size: 13px; color: #515151">@wl &#8491</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
            <span style="font-size: 13px; color: #515151;">@wavg_resid</span>
        </div>
    </div>
"""

skr_hover=HoverTool(tooltips=skr_tooltip, mode='vline')
wavg_hover=HoverTool(tooltips=wavg_tooltip, mode='vline')


skyres_source = ColumnDataSource(
                data={'wl': skyresid['WAVELENGTH'],
                      'med_resid' : skyresid['MED_RESID_WAVE'],
                      'wavg_resid':  skyresid['WAVG_RES_WAVE']
                     })

p1 = figure(title= 'MED_RESID_WAVE', 
            x_axis_label='Angstrom', y_axis_label="Units",
            plot_width = 720, plot_height = 240,
          tools=[skr_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

p1.line('wl', 'med_resid', source=skyres_source)

p2 = figure(title= 'WAVG_RESID_WAVE', 
            x_axis_label='Angstrom', y_axis_label="Units",
            plot_width = 720, plot_height = 240,
          tools=[wavg_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

p2.line('wl', 'wavg_resid', source=skyres_source)


'''p1.circle('wl', 'med_resid', source=skyres_source, alpha = 0, size=1,
          hover_alpha=1,
         hover_fill_color='orange', hover_line_color='red') '''

'''p2.circle('wl', 'wavg_resid', source=skyres_source, alpha=0, size=1,
         hover_alpha=1,
          hover_fill_color='orange', hover_line_color='red')''' 



p1.x_range = p2.x_range

info, nlines = write_info('skyresid', tests['skyresid'])
txt = PreText(text=info, height=nlines*20, width=p2.plot_width)
p2txt = column(widgetbox(txt), p1, p2)

#layout=column(p1,p2)
curdoc().add_root(p2txt)
curdoc().title = "SKYRESID"
