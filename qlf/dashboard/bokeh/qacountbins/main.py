from bokeh.plotting import figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import (LinearColorMapper ,    ColorBar)


from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

from bokeh.io import output_notebook
import numpy as np

from dashboard.bokeh.helper import get_url_args

import ast

import numpy as np
import logging

logger = logging.getLogger(__name__)

# =============================================
# THIS comes from INTERFACE
#
args = get_url_args(curdoc)

selected_exposure = args['exposure']
selected_arm = args['arm']
selected_spectrograph = args['spectrograph']

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

# =============================================
# THIS is only to simplify the code understanding
#
countpix  = metrics['countpix']
getbias   = metrics['getbias']
getrms    = metrics['getrms']
xwsigma   = metrics['xwsigma']
countbins = metrics['countbins']
integ     = metrics['integ']
skycont   = metrics['skycont']
skypeak   = metrics['skypeak']
skyresid  = metrics['skyresid']
snr       = metrics['snr']


countbins = ast.literal_eval(countbins)

# ============================================
# THIS: Given the set up in the block above, 
#       we have the bokeh plots


hist_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Frequency: </span>
            <span style="font-size: 13px; color: #515151">@hist</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">sigma: </span>
            <span style="font-size: 13px; color: #515151;">[@left, @right]</span>
        </div>
    </div>
"""
name_hi = 'NBINSHIGH'
name_med = 'NBINSMED'
name_low = 'NBINSLOW'

def bins_doane(data):
    # Dane's rule of thumb for bins
    ndata = len(data)
    mean = np.mean(data)
    sigma = np.std(data)
    b = sum([ (x - mean)**3 for x in data])
    b = b/sum([ (x - mean)**2 for x in data])**(1.5)
    try:
        return int(round(np.log2(ndata) + 1 + np.log2((1.+b)/(sigma*b))))
    except:
        return int(round(np.log2(ndata) + 1 ))
    
bins_hi = bins_doane(countbins[name_hi])
bins_med = bins_doane(countbins[name_med])
bins_low = bins_doane(countbins[name_low])# formely: 17
hover = HoverTool(tooltips=hist_tooltip)
hover2 = HoverTool(tooltips=hist_tooltip)
hover3 = HoverTool(tooltips=hist_tooltip)


# ===
hist_hi, edges_hi = np.histogram(countbins[name_hi], bins = bins_hi)
source_hi = ColumnDataSource(data={
    'hist':hist_hi,
    'bottom':[0] *len(hist_hi),
    'left':edges_hi[:-1],
    'right':edges_hi[1:]
})

# ===
hist_med, edges_med = np.histogram(countbins[name_med], bins = bins_med)
source_med = ColumnDataSource(data={
    'hist':hist_med,
    'bottom':[0] *len(hist_med),
    'left':edges_med[:-1],
    'right':edges_med[1:]
})

# ===
hist_low, edges_low = np.histogram(countbins[name_low], bins = bins_low)
source_low = ColumnDataSource(data={
    'hist':hist_low,
    'bottom':[0] *len(hist_low),
    'left':edges_low[:-1],
    'right':edges_low[1:]
})



phi = figure(title='NBINSHI',tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")

phi.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_hi, 
        fill_color="dodgerblue", line_color="black", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

pmed = figure(title='NBINSMED',tools=[hover2,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")

pmed.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_med, 
        fill_color="lightgreen", line_color="black", alpha=0.8,
       hover_fill_color='green', hover_line_color='black', hover_alpha=0.8)


plow = figure(title='NBINSLOW',tools=[hover3,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")


plow.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_low, fill_color="tomato", line_color="black", alpha=0.8,
       hover_fill_color='red', hover_line_color='black', hover_alpha=0.8)

#plow.legend.location = "top_left"
layout = gridplot( [phi,pmed,plow,None], ncols=2, plot_width=600, plot_height=600)


# End of Bokeh Block
curdoc().add_root(layout)