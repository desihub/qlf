import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models.widgets import PreText, Div
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.models import (LinearColorMapper ,    ColorBar)


from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

from bokeh.io import output_notebook
import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description, write_info, get_scalar_metrics,\
                            eval_histpar

import numpy as np
import logging

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

getbias   = metrics['getbias']

# ============================================
# THIS: Given the set up in the block above, 
#       we have the bokeh plots

# Get Bias
name = 'BIAS_AMP'
metr = getbias

dx = [0,1,0,1]
dy = [1,1,0,0]
dz = metr[name] #getbias['BIAS_AMP']

mapper = LinearColorMapper(palette= Viridis256, low=min(dz),high=max(dz) )

dzmax, dzmin = max(dz), min(dz) 
if np.log10(dzmax) > 4 or np.log10(dzmin) <-3:
    ztext = ['{:3.2e}'.format(i) for i in dz]
    cbarformat = "%2.1e"
elif np.log10(dzmin)>0:
    ztext = ['{:4.3f}'.format(i) for i in dz]
    cbarformat = "%4.2f"
else:
    ztext = ['{:5.4f}'.format(i) for i in dz]
    cbarformat = "%5.4f"


source = ColumnDataSource(
    data=dict(
        x=dx,
        y=dy,
        y_offset1 = [i+0.15 for i in dy],
        y_offset2 = [i-0.05 for i in dy],

        z = dz,
        amp = ['AMP %s'%i for i in range(1,5) ] ,
        ztext = ztext#['{:3.2e}'.format(i) for i in dz]
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
#[         ("counts", "@z"),
#         ("AMP", "@amp"),         ])

p = Figure(title=name, tools=[hover],
           x_range= list([-0.5,1.5]),           # length = 18
           y_range= list([-0.5,1.5]), #numeros romanos
           plot_width=450, plot_height=400
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
formatter = PrintfTickFormatter(format=cbarformat)#format='%2.1e')
color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                major_label_text_font_size='10pt', label_standoff=2, location=(0, 0)
                   ,formatter=formatter, title="(ADU)", title_text_baseline="alphabetic" )

p.add_layout(color_bar, 'right')


p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks


#-------------------------------------
# histogram


yscale = "auto"#"auto" or "log"

hist_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Frequency: </span>
            <span style="font-size: 13px; color: #515151">@hist</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">XSIGMA: </span>
            <span style="font-size: 13px; color: #515151;">[@left, @right]</span>
        </div>
    </div>
"""

hist, edges  = np.histogram(getbias['MEANBIAS_ROW'], bins='sqrt')

source_hist = ColumnDataSource(data={
    'hist': hist,
    'histplusone':np.array(hist)+1,
    'bottom':[0] *len(hist),
    'bottomplusone':[1]*len(hist),
    'left':edges[:-1],
    'right':edges[1:]
})

hover = HoverTool(tooltips=hist_tooltip)

ylabel,yrange,bottomval,histval = eval_histpar(yscale, hist)

xhistlabel = "MEANBIAS_ROW"
p_hist = Figure(title='',tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label=ylabel, x_axis_label=xhistlabel, background_fill_color="white"
        , plot_width=700, plot_height=400
        , x_axis_type="auto",    y_axis_type=yscale
        , y_range=yrange)#, y_range=(1, 11**(int(np.log10(max(hist)))+1) ) )

p_hist.quad(top=histval, bottom=bottomval, left='left', right='right',
       source=source_hist, 
        fill_color="dodgerblue", line_color="blue", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)



#infos
info, nlines = write_info('getbias', tests['getbias'])
info_hist ="""
<p style="font-size:18px;"> BIAS: {} </p>
""".format(getbias['BIAS'])
txt = Div(text=info_hist, width= 2*p.plot_width)


info_col=Div(text=write_description('getbias'), width=2*p.plot_width)
ptxt = column(widgetbox(info_col), p, txt,p_hist)


#output_notebook()

# End of Bokeh Block
curdoc().add_root(ptxt)
curdoc().title="GETBIAS"
