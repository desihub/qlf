import os
import sys

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL
from bokeh.plotting import Figure
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import row, column, widgetbox, gridplot
from bokeh.models import (LinearColorMapper ,    ColorBar)
from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter, Spacer
from dashboard.bokeh.helper import write_description, write_info, \
    get_scalar_metrics
from dashboard.bokeh.helper import get_palette

from dashboard.bokeh.helper import get_data, get_exposure_ids, \
    init_xy_plot, get_url_args, get_arms_and_spectrographs


import numpy as np


QLF_API_URL = os.environ.get(
    'QLF_API_URL',
    'http://localhost:8000/dashboard/api'
)

# Get url query args
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
    metrics, tests = lm['results']['metrics'], lm['results']['tests']
    print(metrics.keys())
except:
    sys.exit('Could not load metrics')

snr = metrics['snr']

try:
    exptime = tests['checkHDUs']['EXPTIME']
    name_warn=[]
except:
    exptime=1000
    name_warn = '(exptime fixed)'
    print('EXPTIME NOT FOUND, USING 1000')

print(lm.keys())
print(lm['results'].keys())
print(lm['results']['metrics'].keys(), lm['results']['tests'].keys())

#sort the correct vector:
fiberlen = []
snrlen = []
for i, key in enumerate(['ELG_FIBERID', 'LRG_FIBERID','QSO_FIBERID', 'STAR_FIBERID']):
    fiberlen.append( len(snr[key]))
    snrlen.append( len(snr['SNR_MAG_TGT'][i][0]) )
try:
    sort_idx=[ snrlen.index(fiberlen[i]) for i in range(4)]
except:
    sys.exit('Inconsistence in FIBERID and SNR lenght')        

elg_snr  = snr['SNR_MAG_TGT'][sort_idx[0]] #[2]
lrg_snr  = snr['SNR_MAG_TGT'][sort_idx[1]] #[0]
qso_snr  = snr['SNR_MAG_TGT'][sort_idx[2]] #[1]
star_snr = snr['SNR_MAG_TGT'][sort_idx[3]] #[3]


def fit_func(xdata, coeff):
    """ astro fit 
    """
    r1=0.0 #read noise
    a, b = coeff

    x = np.linspace(min(xdata), max(xdata), 1000)
    Flux = 10**(-0.4*(x - 22.5))
    y = a*Flux*exptime/np.sqrt( a*Flux*exptime + b*exptime+r1**2) 
    return x, y



data_model = {
    'x': [],
    'y': [],
    'logy': [],
    'fiber_id': [],
    'ra': [],
    'dec': []
}

elg = ColumnDataSource(data=data_model.copy())
lrg = ColumnDataSource(data=data_model.copy())
qso = ColumnDataSource(data=data_model.copy())
star = ColumnDataSource(data=data_model.copy())

data_fit = {
    'x': [],
    'y': [],
    'logy': [],
    'fiber_id': [],
    'ra': [],
    'dec': []
}
elg_fit = ColumnDataSource(data=data_fit.copy())
lrg_fit = ColumnDataSource(data=data_fit.copy())
qso_fit = ColumnDataSource(data=data_fit.copy())
star_fit = ColumnDataSource(data=data_fit.copy())

elg.data['x'] = elg_snr[1] 
elg.data['y'] = elg_snr[0] 
elg.data['logy'] = np.log10(np.array(elg_snr[0]))
elg.data['fiber_id'] = snr['ELG_FIBERID']
elg.data['ra'] = [snr['RA'][i] for i in snr['ELG_FIBERID'] ]
elg.data['dec'] = [snr['DEC'][i] for i in snr['ELG_FIBERID'] ]

lrg.data['x'] = lrg_snr[1] 
lrg.data['y'] = lrg_snr[0] 
lrg.data['logy'] = np.log10(np.array(lrg_snr[0]))
lrg.data['fiber_id'] = snr['LRG_FIBERID']
lrg.data['ra'] = [snr['RA'][i] for i in snr['LRG_FIBERID'] ]
lrg.data['dec'] = [snr['DEC'][i] for i in snr['LRG_FIBERID'] ]

qso.data['x'] = qso_snr[1] 
qso.data['y'] = qso_snr[0] 
qso.data['logy'] = np.log10(np.array(qso_snr[0]))
qso.data['fiber_id'] = snr['QSO_FIBERID']
qso.data['ra'] = [snr['RA'][i] for i in snr['QSO_FIBERID'] ]
qso.data['dec'] = [snr['DEC'][i] for i in snr['QSO_FIBERID'] ]

star.data['x'] = star_snr[1] 
star.data['y'] = star_snr[0] 
star.data['logy'] = np.log10(np.array(star_snr[0]))
star.data['fiber_id'] = snr['STAR_FIBERID']
star.data['ra'] = [snr['RA'][i] for i in snr['STAR_FIBERID'] ]
star.data['dec'] = [snr['DEC'][i] for i in snr['STAR_FIBERID'] ]


xfit, yfit  = fit_func(elg_snr[1], 		snr['FITCOEFF_TGT'][sort_idx[0]])
elg_fit.data['x'] = xfit
elg_fit.data['logy'] = np.log10(yfit)
elg_fit.data['y'] = (yfit)
for key in ['fiber_id', 'ra', 'dec']:
    elg_fit.data[key] = ['']*len(yfit)

xfit, yfit = fit_func(lrg_snr[1], snr['FITCOEFF_TGT'][sort_idx[1]])
lrg_fit.data['x'] = xfit
lrg_fit.data['logy'] = np.log10(yfit)
lrg_fit.data['y'] = yfit
for key in ['fiber_id', 'ra', 'dec']:
    lrg_fit.data[key] = ['']*len(yfit)

xfit, yfit = fit_func(qso_snr[1], snr['FITCOEFF_TGT'][sort_idx[2]])
qso_fit.data['x'] = xfit
qso_fit.data['logy'] = np.log10(yfit)
qso_fit.data['y'] = yfit
for key in ['fiber_id', 'ra', 'dec']:
    qso_fit.data[key] = ['']*len(yfit)

xfit, yfit = fit_func( star_snr[1], snr['FITCOEFF_TGT'][sort_idx[3]])
star_fit.data['x'] = xfit
star_fit.data['logy'] = np.log10(yfit)
star_fit.data['y'] = yfit
for key in ['fiber_id', 'ra', 'dec']:
    star_fit.data[key] = ['']*len(yfit)

# here we make the plots
html_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">SNR: </span>
            <span style="font-size: 13px; color: #515151;">@y</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">DECAM_R: </span>
            <span style="font-size: 13px; color: #515151;">@x</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Fiber ID: </span>
            <span style="font-size: 13px; color: #515151;">@fiber_id</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
            <span style="font-size: 13px; color: #515151;">@ra</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Dec: </span>
            <span style="font-size: 13px; color: #515151">@dec</span>
        </div>
    </div>
"""

url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

lw=1.5
y_plot = 'y'
plt_scale = 'log'

hover = HoverTool(tooltips=html_tooltip)
elg_plot = init_xy_plot(hover=hover, yscale=plt_scale)
elg_plot.line(x='x', y=y_plot,source=elg_fit, color="black", line_width=lw, line_alpha=0.9)
elg_plot.circle(x='x', y=y_plot, source=elg, color="blue", size=8, line_color='black', alpha=0.7
            ,hover_color="blue", hover_alpha=1, hover_line_color='red')

elg_plot.xaxis.axis_label = "DECAM_R"
elg_plot.yaxis.axis_label = "MEDIAN SNR"
elg_plot.title.text = "ELG"

taptool = elg_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

hover = HoverTool(tooltips=html_tooltip)
lrg_plot = init_xy_plot(hover=hover, yscale=plt_scale)
lrg_plot.line(x='x', y=y_plot, source=lrg_fit, color="black", line_width=lw, line_alpha=0.9)
lrg_plot.circle(x='x', y=y_plot, source=lrg, color="red", size=8, line_color='black', alpha=0.7
            , hover_color="red",hover_alpha=1, hover_line_color='red')

lrg_plot.xaxis.axis_label = "DECAM_R"
lrg_plot.yaxis.axis_label = "MEDIAN SNR"
lrg_plot.title.text = "LRG"

taptool = lrg_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

hover = HoverTool(tooltips=html_tooltip)
qso_plot = init_xy_plot(hover=hover, yscale=plt_scale)
qso_plot.line(x='x', y=y_plot, source=qso_fit, color="black", line_width=lw, line_alpha=0.9)
qso_plot.circle(x='x', y=y_plot, source=qso, color="green", size=8, line_color='black', alpha=0.7
            ,hover_color="green", hover_alpha=1, hover_line_color='red')

qso_plot.xaxis.axis_label = "DECAM_R"
qso_plot.yaxis.axis_label = "MEDIAN SNR"
qso_plot.title.text = "QSO"

taptool = qso_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

hover = HoverTool(tooltips=html_tooltip)
star_plot = init_xy_plot(hover=hover, yscale=plt_scale)
star_plot.line(x='x', y=y_plot, source=star_fit, color="black", line_width=lw, line_alpha=0.9)
star_plot.circle(x='x', y=y_plot, source=star, color="orange", size=8, line_color='black', alpha=0.7
            ,hover_color="orange", hover_alpha=1, hover_line_color='red')

star_plot.xaxis.axis_label = "DECAM_R"
star_plot.yaxis.axis_label = "MEDIAN SNR"
star_plot.title.text = "STAR"

#taptool = star_plot.select(type=TapTool)
#taptool.callback = OpenURL(url=url)


r1=row(children=[elg_plot, lrg_plot], sizing_mode='fixed') 
r2=row( children=[qso_plot, star_plot], sizing_mode='fixed')
plot = column([r1,r2], sizing_mode='fixed')
# infos
key_name = 'snr'
info, nlines = write_info(key_name, tests[key_name])
txt = PreText(text=info, height=nlines*20)
info_col = Div(text=write_description('snr'), width= 1400)#*star_plot.plot_width)


#---------------
#wedges


snr_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Resid: </span>
            <span style="font-size: 13px; color: #515151">@resid_snr</span>
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
            <span style="font-size: 13px; color: #515151;">@QLF_FIBERID</span>
        </div>

    </div>
"""
snr_hover = HoverTool(tooltips=snr_tooltip)
snr = metrics['snr']
skycont=metrics['skycont']
median = snr['MEDIAN_SNR']
resid = snr['SNR_RESID']
qlf_fiberid = range(0,500)
my_palette = get_palette('bwr')

obj_type = []
fibersnr = []
for i in qlf_fiberid:
    if i in snr['ELG_FIBERID']:
        obj_type.append('ELG')
        fibersnr.append(i) 
    elif i in snr['QSO_FIBERID']:
        obj_type.append('QSO')
        fibersnr.append(i)
    elif i in snr['LRG_FIBERID']:
        obj_type.append('LRG')
        fibersnr.append(i)
    elif i in snr['STAR_FIBERID']:
        obj_type.append('STAR')
        fibersnr.append(i)
    elif i in skycont['SKYFIBERID']:
        obj_type.append('SKY')
    else:
        obj_type.append('UNKNOWN')


source = ColumnDataSource(data={
    'x1': [snr['RA'][i] for i in fibersnr ],
    'y1': [snr['DEC'][i] for i in fibersnr ],
    'resid_snr': snr['SNR_RESID'],
    'QLF_FIBERID': fibersnr,
    'OBJ_TYPE': [obj_type[i] for i in fibersnr],

})


dy = (np.max(resid) - np.min(resid))*0.02
mapper = LinearColorMapper(palette=my_palette,
                           low=np.min(resid)- dy, high= np.max(resid)+dy)
radius = 0.013#0.015
radius_hover = 0.015#0.0165

# axes limit
xmin, xmax = [min(snr['RA'][:]), max(snr['RA'][:])]
ymin, ymax = [min(snr['DEC'][:]), max(snr['DEC'][:])]
xfac, yfac  = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
left, right = xmin -xfac, xmax+xfac
bottom, top = ymin-yfac, ymax+yfac

p = Figure(title='Residual SNR'+name_warn
        , x_axis_label='RA', y_axis_label='DEC'
        , plot_width=700, plot_height=550
        , tools=[snr_hover, "pan,box_zoom,reset,crosshair, tap"])
# Color Map
p.circle('x1', 'y1', source=source, name="data", radius=radius,
         fill_color={'field': 'resid_snr', 'transform': mapper},
         line_color='black', line_width=0.4,
         hover_line_color='red')

# marking the Hover point
p.circle('x1', 'y1', source=source, name="data", radius=radius_hover, hover_fill_color={
         'field': 'resid_snr', 'transform': mapper}, fill_color=None, line_color=None, line_width=3, hover_line_color='red')

xcolor_bar = ColorBar(color_mapper=mapper, label_standoff=13,
                      title="",
                      major_label_text_font_style="bold", padding=26,
                      major_label_text_align='right',
                      major_label_text_font_size="10pt",
                      location=(0, 0))

p.add_layout(xcolor_bar, 'right')

#plot= gridplot([[elg_plot, lrg_plot], [qso_plot, star_plot]])

layout = column(widgetbox(info_col),p, row(plot, Spacer(width=700, height=500)), sizing_mode='fixed')





curdoc().add_root(layout)
curdoc().title = "MEDIAN SNR"
