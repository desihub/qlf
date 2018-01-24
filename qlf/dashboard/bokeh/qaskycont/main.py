from bokeh.plotting import figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import (LinearColorMapper ,    ColorBar)

import ast

from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

from bokeh.io import output_notebook
import numpy as np

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

skc_tooltips = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">SKY CONT: </span>
            <span style="font-size: 13px; color: #515151;">@skycont</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
            <span style="font-size: 13px; color: #515151;">@ra</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
            <span style="font-size: 13px; color: #515151;">@dec</span>
        </div>
    </div>
"""
c1,c2 = int(selected_spectrograph)*500, (int(selected_spectrograph)+1)*500
qlf_fiberid = np.arange(0,5000)[c1:c2] 

hover = HoverTool(tooltips=skc_tooltips)

# sky continuum per sky fiber averaged over two continuum regions,
#  'n' is number of sky fibers
skycont =ast.literal_eval(skycont)
sky = skycont['SKYCONT_FIBER']
skyfibers = skycont['SKYFIBERID']

ra = [ skycont['RA'][c1:c2][i] for i in skyfibers]
dec = [ skycont['DEC'][c1:c2][i] for i in skyfibers]

ra_not, dec_not=[],[]
for i in range(500):
    if i not in skyfibers:
        ra_not.append(skycont['RA'][c1:c2][i])
        dec_not.append(skycont['DEC'][c1:c2][i])

source2 = ColumnDataSource(data={
                'skycont' : sky,
                'fiberid' : skyfibers,
                'ra'  : ra,
                'dec' : dec
})

source2_not = ColumnDataSource(data={
            'ra':ra_not,
            'dec':dec_not,
            'skycont': ['']*len(dec_not)
            })
        
mapper = LinearColorMapper(palette= my_palette,
                           low = np.min(sky), 
                           high = np.max(sky))
p2 = figure(title='SKY_CONT', 
            x_axis_label='RA', y_axis_label='DEC',
            plot_width=700, plot_height=600,
            tools= [hover, "pan,box_zoom,reset"])

p2.circle('ra','dec', source=source2, radius=0.016,
        fill_color={'field': 'skycont', 'transform': mapper}, 
         line_color='black', line_width=0.1)

# marking the Hover point
p2.circle('ra','dec', source = source2, radius = 0.0186
          , fill_color=None, line_color=None
          , hover_fill_color={'field': 'skycont', 'transform': mapper}
          , line_width=3, hover_line_color='red')


p2.circle('ra', 'dec', source= source2_not, radius=0.015, 
            fill_color = 'lightgray', line_color='black', line_width=0.3)

# marking the Hover point
p2.circle('ra','dec', source = source2_not, radius = 0.0186
          , fill_color=None, line_color=None
          , line_width=3, hover_line_color='red', hover_fill_color='lightgrey')


color_bar = ColorBar(color_mapper= mapper, label_standoff=-13,
                     major_label_text_font_style='bold', padding = 26,
                     major_label_text_align='right',
                     major_label_text_font_size="10pt",
                     location=(0, 0))
p2.add_layout(color_bar)




# End of Bokeh Block
curdoc().add_root(p2)