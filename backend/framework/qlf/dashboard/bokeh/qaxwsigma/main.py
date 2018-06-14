import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import ColumnDataSource, HoverTool, Range1d, OpenURL
from bokeh.models import LinearColorMapper , ColorBar
from bokeh.models.widgets import Select, Slider
from dashboard.bokeh.helper import get_url_args, write_description, get_scalar_metrics
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import plot_hist

from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import PreText, Div

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

xwsigma   = metrics['xwsigma']
snr       = metrics['snr'] #RA and DEC info
skycont   = metrics['skycont']


my_palette = get_palette("viridis") #"seismic")#"RdYlBu_r")#"viridis")


xsigma_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">XSigma: </span>
            <span style="font-size: 13px; color: #515151">@xsigma</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
            <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
            <span style="font-size: 13px; color: #515151;">@x1</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
            <span style="font-size: 13px; color: #515151;">@y1</span>
        </div>

        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER #: </span>
            <span style="font-size: 13px; color: #515151;">@xfiber</span>
        </div>

    </div>
"""

wsigma_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">WSigma: </span>
            <span style="font-size: 13px; color: #515151">@wsigma</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
            <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
            <span style="font-size: 13px; color: #515151;">@x1</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
            <span style="font-size: 13px; color: #515151;">@y1</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER #: </span>
            <span style="font-size: 13px; color: #515151;">@wfiber</span>
        </div>

    </div>
"""

url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

# determining the position of selected cam fibers:
c1,c2 = 0,500 #int(selected_spectrograph)*500, (int(selected_spectrograph)+1)*500
qlf_fiberid = np.arange(0,5000)[c1:c2] 
try:
    snr = metrics['snr']
except:
    snr= {'ELG_FIBERID':[],'QSO_FIBERID':[],
          'LRG_FIBERID':[],'STAR_FIBERID':[]}
try:
    skycont = metrics['skycont']
except:
    skycont ={'SKYFIBERID':[]}
# marking type of objects:
obj_type=[]
for i in range(500):
    if  i in snr['ELG_FIBERID']:
        obj_type.append('ELG')
    elif  i  in snr['QSO_FIBERID']:
        obj_type.append('QSO')
    elif  i  in snr['LRG_FIBERID']:
        obj_type.append('LRG')
    elif  i in snr['STAR_FIBERID']:
        obj_type.append('STAR')
    elif i in skycont['SKYFIBERID']:
        obj_type.append('SKY')
    else:
        obj_type.append('UNKNOWN')
# ---------------------------------


xsigma_hover = HoverTool(tooltips=xsigma_tooltip)
wsigma_hover = HoverTool(tooltips=wsigma_tooltip)


xsigma = xwsigma['XWSIGMA_FIB'][0]
wsigma = xwsigma['XWSIGMA_FIB'][1]
xfiber = np.arange(len(xsigma))
wfiber = np.arange(len(wsigma))




source = ColumnDataSource(data={
    'x1'     : snr['RA'], #xwsigma['RA'][c1:c2],
    'y1'     : snr['DEC'], #xwsigma['DEC'][c1:c2],
    'xsigma' : xsigma,
    'wsigma' : wsigma,
    'xfiber': xfiber,
    'wfiber': wfiber,
    'OBJ_TYPE': obj_type,
    'left': np.arange(0,500)-0.4,
    'right': np.arange(0,500)+0.4,
    'bottom': [0]*500
})

'''
source_comp = ColumnDataSource(
    data = {
    'x1': xwsigma['RA'][:c1] + xwsigma['RA'][c2:],
    'y1': xwsigma['DEC'][:c1] + xwsigma['DEC'][c2:],
    'xsigma': ['']*4500,
    'wsigma': ['']*4500
})
'''

# axes limit
xmin, xmax = [min(snr['RA'][:]), max(snr['RA'][:])]
ymin, ymax = [min(snr['DEC'][:]), max(snr['DEC'][:])]
xfac, yfac  = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
left, right = xmin -xfac, xmax+xfac
bottom, top = ymin-yfac, ymax+yfac

xmapper = LinearColorMapper(palette= my_palette,
                           low=0.98*np.min(xsigma), 
                           high=1.02*np.max(xsigma))

wmapper = LinearColorMapper(palette= my_palette,
                           low=0.99*np.min(wsigma), 
                           high=1.01*np.max(wsigma))

# ======
# XSIGMA

radius = 0.015
radius_hover = 0.0165

px = Figure( title = 'XSIGMA', x_axis_label='RA', y_axis_label='DEC'
           , plot_width=700, plot_height=550
           , x_range=Range1d(left, right), y_range=Range1d(bottom, top)
           , tools= [xsigma_hover, "pan,box_zoom,reset,crosshair, tap"])

# Color Map
px.circle('x1','y1', source = source, name="data", radius = radius,
        fill_color={'field': 'xsigma', 'transform': xmapper}, 
         line_color='black', line_width=0.1,
         hover_line_color='red')

# marking the Hover point
px.circle('x1','y1', source = source, name="data", radius = radius_hover
          , hover_fill_color={'field': 'xsigma', 'transform': xmapper}
          , fill_color=None, line_color=None
          , line_width=3, hover_line_color='red')

'''
px.circle('x1','y1', source = source_comp, radius = radius_hover,
         fill_color = 'lightgray', line_color='black', line_width=0.3)
'''
taptool = px.select(type=TapTool)
taptool.callback = OpenURL(url=url)

xcolor_bar = ColorBar(color_mapper= xmapper, label_standoff=-13,
                     major_label_text_font_style="bold", padding = 26,
                     major_label_text_align='right',
                     major_label_text_font_size="10pt",
                     location=(0, 0))

px.add_layout(xcolor_bar, 'left')


# x_fiber_hist
d_yplt = (max(xsigma) - min(xsigma))*0.1
yrange = [0, max(xsigma) +d_yplt]

xhist = plot_hist(xsigma_hover, yrange, ph=280)
xhist.quad(top='xsigma', bottom='bottom', left='left', right='right', name='data',source=source,
            fill_color="dodgerblue", line_color="black", line_width =0.01, alpha=0.8,
            hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)

xhist.xaxis.axis_label="Fiber number"
xhist.yaxis.axis_label="X std dev (number of pixels)"


# ======
# WSIGMA
pw = Figure( title = 'WSIGMA', x_axis_label='RA', y_axis_label='DEC'
           , plot_width=700, plot_height=550
           , x_range=Range1d(left, right), y_range=Range1d(bottom, top)
           , tools= [wsigma_hover, "pan,box_zoom,reset,crosshair,tap"])

# Color Map
pw.circle('x1','y1', source = source, name="data", radius = radius,
        fill_color={'field': 'wsigma', 'transform': wmapper}, 
         line_color='black', line_width=0.1,
         hover_line_color='red')

# marking the Hover point
pw.circle('x1','y1', source = source, name="data", radius = radius_hover
          , hover_fill_color={'field': 'wsigma', 'transform': wmapper}
          , fill_color=None, line_color=None
          , line_width=3, hover_line_color='red')
'''
pw.circle('x1','y1', source = source_comp, radius = 0.015,
         fill_color = 'lightgray', line_color='black', line_width=0.3)
'''
taptool = pw.select(type=TapTool)
taptool.callback = OpenURL(url=url)


# bokeh.pydata.org/en/latest/docs/reference/models/annotations.html
wcolor_bar = ColorBar(color_mapper= wmapper, label_standoff=-13,
                     major_label_text_font_style="bold", padding = 26,
                     major_label_text_align='right',
                     major_label_text_font_size="10pt",
                     location=(0, 0))

pw.add_layout(wcolor_bar, 'left')

# w_fiber_hist
d_yplt = (max(wsigma) - min(wsigma))*0.1
yrange = [0, max(wsigma) +d_yplt]

whist = plot_hist(wsigma_hover, yrange, ph=280)
whist.quad(top='wsigma', bottom='bottom', left='left', right='right', name='data',source=source,
            fill_color="dodgerblue", line_color="black", line_width =0.01, alpha=0.8,
            hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
whist.xaxis.axis_label="Fiber number"
whist.yaxis.axis_label="W std dev (number of pixels)"



# ================================
# Stat histogram

def histpar(yscale, hist):
    if yscale == 'log':
        ylabel = "Frequency + 1"
        yrange = (1, 11**(int(np.log10(max(hist)))+1) )
        bottomval = 'bottomplusone'
        histval = 'histplusone'
    else:
        ylabel = "Frequency"
        yrange = (0, 1.1*max(hist))
        bottomval = 'bottom'
        histval = 'hist'
    return [ylabel,yrange,bottomval,histval]


xhistlabel= "XSIGMA"
yscale = "auto"

hist_tooltip_x = """
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


hist, edges = np.histogram(xsigma,'sqrt')# auto: Maximum of the ‘sturges’ and ‘fd’ estimators.

source_hist = ColumnDataSource(data={
    'hist': hist,
    'histplusone':hist+1,
    'bottom':[0] *len(hist),
    'bottomplusone':[1]*len(hist),
    'left':edges[:-1],
    'right':edges[1:]
})

hover = HoverTool(tooltips=hist_tooltip_x)

ylabel,yrange,bottomval,histval = histpar(yscale, hist)

p_hist_x = Figure(title='',tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label= ylabel, x_axis_label=xhistlabel, background_fill_color="white"
        , plot_width=700, plot_height=400
        , x_axis_type="auto",    y_axis_type=yscale
        , y_range=yrange)#, y_range=(1, 11**(int(np.log10(max(hist)))+1) ) )

p_hist_x.quad(top=histval, bottom=bottomval, left='left', right='right',
       source=source_hist, 
        fill_color="dodgerblue", line_color="black", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

# Histogram 2
xhistlabel= "WSIGMA"
hist_tooltip_w = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Frequency: </span>
            <span style="font-size: 13px; color: #515151">@hist</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">WSIGMA: </span>
            <span style="font-size: 13px; color: #515151;">[@left, @right]</span>
        </div>
    </div>
"""


hist, edges = np.histogram(wsigma, 'sqrt')

source_hist = ColumnDataSource(data={
    'hist': hist,
    'histplusone':hist+1,
    'bottom':[0] *len(hist),
    'bottomplusone':[1]*len(hist),
    'left':edges[:-1],
    'right':edges[1:]
})

hover = HoverTool(tooltips=hist_tooltip_w)

ylabel,yrange,bottomval,histval = histpar(yscale, hist)

p_hist_w = Figure(title='',tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label=ylabel, x_axis_label=xhistlabel, background_fill_color="white"
        , plot_width=700, plot_height=400
        , x_axis_type="auto",    y_axis_type=yscale
        ,y_range=yrange)#, y_range=(1, 11**(int(np.log10(max(hist)))+1) ) )

p_hist_w.quad(top= histval, bottom=bottomval, left='left', right='right',
       source=source_hist, 
        fill_color="dodgerblue", line_color="black", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)


#--------------------------------------------------------------------------
#AMP Plots
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import set_amp, plot_amp
from bokeh.models import PrintfTickFormatter

dz = xwsigma['XWSIGMA_AMP'][0]
name = 'XSIGMA AMP'
Reds = get_palette('Reds')
mapper = LinearColorMapper(palette= Reds, low=min(dz),high=max(dz) )

ztext, cbarformat = set_amp(dz)
xamp = plot_amp(dz, mapper,name=name)

formatter = PrintfTickFormatter(format=cbarformat)
color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                formatter=formatter, title="", title_text_baseline="alphabetic" )
xamp.height=400
xamp.width =500
xamp.add_layout(color_bar, 'right')


dz = xwsigma['XWSIGMA_AMP'][1]
name = 'WSIGMA AMP'
Reds = get_palette('Reds')
mapper = LinearColorMapper(palette= Reds, low=min(dz),high=max(dz) )

ztext, cbarformat = set_amp(dz)
wamp = plot_amp(dz, mapper,name=name)

formatter = PrintfTickFormatter(format=cbarformat)
color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                formatter=formatter, title="", title_text_baseline="alphabetic" )
wamp.height=400
wamp.width =500

wamp.add_layout(color_bar, 'right')



# -------------------------------------------------------------------------
from bokeh.models import Spacer

info_col=Div(text=write_description('xwsigma'), width=2*pw.plot_width)
pxh = column(px, xhist, p_hist_x, xamp )
pwh = column(pw, whist, p_hist_w, wamp )
layoutplot= row([pxh, Spacer(width=0),pwh]) #, sizing_mode='scale_width')
layout = column(widgetbox(info_col),layoutplot) #, row( [xamp, Spacer(width=80), wamp]))
 
curdoc().add_root(layout)
curdoc().title = "XWSIGMA"
