from bokeh.plotting import figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import (LinearColorMapper ,    ColorBar)


from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

from bokeh.io import output_notebook
import numpy as np

import ast

from dashboard.bokeh.helper import get_url_args

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

# ============================================
# THIS: Given the set up in the block above, 
#       we have the bokeh plots

name = 'RMS_AMP'
metr = ast.literal_eval(getrms)

# Get Bias
dx = [0,1,0,1]
dy = [1,1,0,0]
dz = metr[name] #getbias['BIAS_AMP']
mapper = LinearColorMapper(palette= Viridis256)


source = ColumnDataSource(
    data=dict(
        x=dx,
        y=dy,
        y_offset1 = [i+0.15 for i in dy],
        y_offset2 = [i-0.05 for i in dy],

        z = dz,
        amp = ['AMP %s'%i for i in range(1,5) ] ,
        ztext = ['{:4.3e}'.format(i) for i in dz]
    )
)

cmap_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">counts: </span>
            <span style="font-size: 13px; color: #515151">@z</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">AMP: </span>
            <span style="font-size: 13px; color: #515151;">@amp</span>
        </div>
    </div>
""".replace("counts:", name+":")

hover = HoverTool(tooltips=cmap_tooltip)


p = figure(title=name, tools=[hover],
           x_range= list([-0.5,1.5]),           # length = 18
           y_range= list([-0.5,1.5]), #numeros romanos
           plot_width=400, plot_height=400
          )


p.grid.grid_line_color = None
p.outline_line_color = None
p.axis.clear

text_props = {
    "source": source,
    "angle": 0,
    "color": "black",
    "text_color":"black",
    "text_align": "center",
    "text_baseline": "middle"
}



p.rect("x", "y", .98, .98, 0, source=source,
       fill_color={'field': 'z', 'transform': mapper}, fill_alpha=0.9)#, color="color")
p.axis.minor_tick_line_color=None

p.text(x="x", y="y_offset2", text="ztext",
       text_font_style="bold", text_font_size="20pt", **text_props)
p.text(x="x", y="y_offset1", text="amp",
        text_font_size="18pt", **text_props)
color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                major_label_text_font_size='10pt', label_standoff=2,location=(1, 0))

p.add_layout(color_bar, 'left')


p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks




# End of Bokeh Block
curdoc().add_root(p)