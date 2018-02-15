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
# values to plot:
name = 'PEAKCOUNT'
metr = ast.literal_eval(skypeak)

# ============================================
# THIS: Given the set up in the block above, 
#       we have the bokeh plots




def palette(name_of_mpl_palette):
    """ Transforms a matplotlib palettes into a bokeh 
    palettes
    """
    from matplotlib.colors import rgb2hex
    import matplotlib.cm as cm
    colormap =cm.get_cmap(name_of_mpl_palette) #choose any matplotlib colormap here
    bokehpalette = [rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    return bokehpalette

my_palette = palette("viridis")

peak_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">PEAKCOUNT: </span>
            <span style="font-size: 13px; color: #515151">@peakcount</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
            <span style="font-size: 13px; color: #515151;">@x1</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
            <span style="font-size: 13px; color: #515151;">@y1</span>
        </div>
    </div>
"""

c1,c2 = int(selected_spectrograph)*500, (int(selected_spectrograph)+1)*500
qlf_fiberid = np.arange(0,5000)[c1:c2] 


peak_hover = HoverTool(tooltips=peak_tooltip)

peakcount = metr['PEAKCOUNT']

source = ColumnDataSource(data={
    'x1'     : metr['RA'][c1:c2],
    'y1'     : metr['DEC'][c1:c2],
    'peakcount' : peakcount,
    'QLF_FIBERID': qlf_fiberid,
})


## axes limit
##  left, right = min(skypeak['RA'][c1:c2]), max(skypeak['RA'][c1:c2])
##  bottom, top = min(skypeak['RA'][c1:c2]), max(skypeak['RA'][c1:c2])#13, 16.7

mapper = LinearColorMapper(palette= my_palette,
                           low=0.98*np.min(peakcount), 
                           high=1.02*np.max(peakcount))


# ======
# XSIGMA
p = figure( title = 'SKYPEAK', x_axis_label='RA', y_axis_label='DEC'
           , plot_width=750, plot_height=700
           ## , x_range=Range1d(left, right), y_range=Range1d(bottom, top)
           , tools= [peak_hover, "pan,box_zoom,reset,crosshair"])

# Color Map
p.circle('x1','y1', source = source, name="data", radius = 0.018,
        fill_color={'field': 'peakcount', 'transform': mapper}, 
         line_color='black', line_width=0.1,
         hover_line_color='red')

# marking the Hover point
p.circle('x1','y1', source = source, name="data", radius = 0.0186
          , hover_fill_color={'field': 'peakcount', 'transform': mapper}
          , fill_color=None, line_color=None
          , line_width=3, hover_line_color='red')

## px.circle('x1','y1', source = source_comp, radius = 0.015,
##         fill_color = 'lightgray', line_color='black', line_width=0.3)

# bokeh.pydata.org/en/latest/docs/reference/models/annotations.html
xcolor_bar = ColorBar(color_mapper= mapper, label_standoff=-13,
                     major_label_text_font_style="bold", padding = 26,
                     major_label_text_align='right',
                     major_label_text_font_size="10pt",
                     location=(0, 0))

p.add_layout(xcolor_bar, 'left')



# End of Bokeh Block
curdoc().add_root(p)
