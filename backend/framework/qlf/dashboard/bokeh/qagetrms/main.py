import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models.widgets import PreText, Div
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.models import (LinearColorMapper ,    ColorBar)

from dashboard.bokeh.qlf_plot import html_table
from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

from bokeh.io import output_notebook
import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description, write_info, get_scalar_metrics
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import set_amp, plot_amp


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

getrms    = metrics['getrms']

Reds = get_palette('Reds')


# amp 1
dz = getrms['NOISE_AMP']
name = 'NOISE_AMP'

mapper = LinearColorMapper(palette= Reds, low=min(dz),high=max(dz) )

ztext, cbarformat = set_amp(getrms['NOISE_AMP'])
p = plot_amp(dz, mapper,name=name)

p.xaxis.axis_label = "NOISE per Amp"

formatter = PrintfTickFormatter(format=cbarformat)
color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                formatter=formatter, title="", title_text_baseline="alphabetic" )
p.add_layout(color_bar, 'right')


# amp 2
dz = getrms['NOISE_OVERSCAN_AMP']
name = 'NOISE_OVERSCAN_AMP'

mapper = LinearColorMapper(palette= Reds, low=min(dz),high=max(dz) )

ztext, cbarformat = set_amp(dz)
p2 = plot_amp(dz, mapper,name=name)

p2.xaxis.axis_label = "NOISE Overscan per Amp"

formatter = PrintfTickFormatter(format=cbarformat)
color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                formatter=formatter, title="", title_text_baseline="alphabetic" )
p2.add_layout(color_bar, 'right')


#infos
nrg= tests['getrms']['NOISE_NORMAL_RANGE']
wrg= tests['getrms']['NOISE_WARN_RANGE']
tb = html_table( nrng=nrg, wrng=wrg  )
tbinfo=Div(text=tb, width=400, height=300)


info, nlines = write_info('getrms', tests['getrms'])
info= """<div> 
<body><p  style="text-align:left; color:#262626; font-size:20px;">
            <b>Get RMS</b> <br>Used to calculate RMS of region of 2D image, including overscan.</body></div>"""
nlines=2
txt = Div(text=info, width=p.plot_width)
info_col=Div(text=write_description('getrms'), width=p.plot_width)
ptxt = column(widgetbox(info_col),row(p, tbinfo))


'''
#-------------------------------------
# histogram


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

#hist, edges  = np.histogram(getrms['RMS_ROW'],'doane') # auto, fd or doane
hist, edges  = np.histogram(getrms['NOISE_ROW'][0],'doane') # auto, fd or doane

source_hist = ColumnDataSource(data={
    'hist': hist,
    'histplusone':np.array(hist)+1,
    'bottom':[0] *len(hist),
    'bottomplusone':[1]*len(hist),
    'left':edges[:-1],
    'right':edges[1:]
})

hover = HoverTool(tooltips=hist_tooltip)

from dashboard.bokeh.helper import eval_histpar
yscale = "log"#"auto" or "log"
ylabel, yrange, bottomval, histval = eval_histpar(yscale, hist)#'Frequency', (0, 1.1*max(hist)), 'bottom','hist'#histpar(yscale, hist)

xhistlabel = "RMS"
p_hist = Figure(title="RMS ROW:  rms of each row in CCD",tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label=ylabel, x_axis_label=xhistlabel, background_fill_color="white"
        , plot_width= 650, plot_height=400
        , x_axis_type="auto",    y_axis_type=yscale
        , y_range=yrange)

p_hist.quad(top=histval, bottom=bottomval, left='left', right='right',
       source=source_hist, 
        fill_color="dodgerblue", line_color="blue", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)



#infos
info, nlines = write_info('getrms', tests['getrms'])
info= """<div> 
<body><p  style="text-align:left; color:#262626; font-size:20px;">
            <b>Get RMS</b> <br>Used to calculate RMS of region of 2D image, including overscan.</body></div>"""
nlines=2
txt = Div(text=info, width=p.plot_width)
info_col=Div(text=write_description('getrms'), width=p.plot_width)
ptxt = column(widgetbox(info_col),p)
layout = column(ptxt, p_hist)
'''
layout=column(ptxt, p2)

# End of Bokeh Block
curdoc().add_root(layout)
curdoc().title="GETRMS"
