import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import (LinearColorMapper ,    ColorBar)


from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

from bokeh.io import output_notebook
import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description, get_scalar_metrics

import numpy as np
import logging

#Additional imports:
from bokeh.models.widgets import Div


logger = logging.getLogger(__name__)

# =============================================
# THIS comes from INTERFACE
#
args = get_url_args(curdoc)

try:
    selected_process_id = args['process_id']
    selected_arm = args['arm']
    selected_spectrograph = args['spectrograph']
except:
    sys.exit('Invalid args')

# ============================================
#  THIS READ yaml files
#

cam = selected_arm+str(selected_spectrograph)
try:
    lm = get_scalar_metrics(selected_process_id, cam)
    metrics, tests  = lm['results']['metrics'], lm['results']['tests']
except:
    sys.exit('Could not load metrics')

countbins = metrics['countbins']



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


hover = HoverTool(tooltips=hist_tooltip)
hover2 = HoverTool(tooltips=hist_tooltip)
hover3 = HoverTool(tooltips=hist_tooltip)
bins_hi, bins_med, bins_low = 'sqrt', 'sqrt', 'sqrt' #‘fd’ (Freedman Diaconis Estimator), ‘doane’, sturges

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



phi = Figure(title='NBINSHI',tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")

phi.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_hi, 
        fill_color="dodgerblue", line_color="black", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

pmed = Figure(title='NBINSMED',tools=[hover2,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")

pmed.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_med, 
        fill_color="lightgreen", line_color="black", alpha=0.8,
       hover_fill_color='green', hover_line_color='black', hover_alpha=0.8)


plow = Figure(title='NBINSLOW',tools=[hover3,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")


plow.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_low, fill_color="tomato", line_color="black", alpha=0.8,
       hover_fill_color='red', hover_line_color='black', hover_alpha=0.8)
# ------------------
# Text Infos
html_str="""
<style>
    table {
        font-family: arial, sans-serif;
        font-size: 12px;
        border-collapse: collapse;
        width: 100%;
    }

    td, th {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #dddddd;
                text-align:center;
    }
    tr:{text-align:center;}
</style>

<div  style="text-align:center;padding-left:20px;padding-top:10px;">
<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>CUT-OFF LOW</td>
    <td> > param0</td>
  </tr>
  <tr>
    <td>CUT-OFF MEDIUM</td>
    <td> > param1</td>
  </tr>
  <tr>
    <td>CUT-OFF HIGH</td>
    <td> > param2</td>
  </tr>
    <tr>
        <th colspan="2"; style="text-align:center">GOOD FIBERS RANGES:</th>
    </tr>
    <tr>
        <td> NORMAL RANGE</td>
        <td> param3</td>
    </tr>
    <tr>
        <td> WARNING RANGE </td>
        <td> param4</td>
    </tr>

</table>
</div>

"""
txt_keys=['CUTLO','CUTMED','CUTHI','NGOODFIB_NORMAL_RANGE', 'NGOODFIB_WARN_RANGE']
for i in range(5):
    html_str=html_str.replace('%s%s'%("param",str(i)), str(tests['countbins'][txt_keys[i]]) )

div=Div(text=html_str, 
        width=400, height=200)
# ---------



# plow.legend.location = "top_left"
# layout = gridplot( [phi,pmed,plow,None], ncols=2, plot_width=600, plot_height=600)

layout_plot = gridplot( [plow,pmed,phi,div], ncols=2, responsive=False, plot_width=600, plot_height=600)
info_col=Div(text=write_description('countbins'), width=1200)
layout = column(widgetbox(info_col), layout_plot)


# End of Bokeh Block
curdoc().add_root(layout)
curdoc().title = "COUNTBINS"

