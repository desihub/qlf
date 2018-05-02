import os
import sys

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.helper import write_description, write_info, \
    get_scalar_metrics


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
except:
    sys.exit('Could not load metrics')

snr = metrics['snr']

def fit_func(xdata, coeff):
    a, b, c = coeff[0]
    x = np.linspace(min(xdata), max(xdata), 1000)
    y = a + b*x + c*x**2
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

elg.data['x'] = snr['ELG_SNR_MAG'][1]
elg.data['y'] = snr['ELG_SNR_MAG'][0]
elg.data['logy'] = np.log10(np.array(snr['ELG_SNR_MAG'][0]))
elg.data['fiber_id'] = snr['ELG_FIBERID']
elg.data['ra'] = snr['RA']
elg.data['dec'] = snr['DEC']


lrg.data['x'] = snr['LRG_SNR_MAG'][1]
lrg.data['y'] = snr['LRG_SNR_MAG'][0]
lrg.data['logy'] = np.log10(np.array(snr['LRG_SNR_MAG'][0]))
lrg.data['fiber_id'] = snr['LRG_FIBERID']
lrg.data['ra'] = snr['RA']
lrg.data['dec'] = snr['DEC']

qso.data['x'] = snr['QSO_SNR_MAG'][1]
qso.data['y'] = snr['QSO_SNR_MAG'][0]
qso.data['logy'] = np.log10(np.array(snr['QSO_SNR_MAG'][0]))
qso.data['fiber_id'] = snr['QSO_FIBERID']
qso.data['ra'] = snr['RA']
qso.data['dec'] = snr['DEC']

star.data['x'] = snr['STAR_SNR_MAG'][1]
star.data['y'] = snr['STAR_SNR_MAG'][0]
star.data['logy'] = np.log10(np.array(snr['STAR_SNR_MAG'][0]))
star.data['fiber_id'] = snr['STAR_FIBERID']
star.data['ra'] = snr['RA']
star.data['dec'] = snr['DEC']

xfit, yfit = fit_func(snr['ELG_SNR_MAG'][1], snr['ELG_FITRESULTS'])
elg_fit.data['x'] = xfit
elg_fit.data['logy'] = yfit
elg_fit.data['y'] = 10**(yfit)
for key in ['fiber_id', 'ra', 'dec']:
    elg_fit.data[key] = ['']*len(yfit)
#elg_fit.stream(elg_fit.data, 30)

xfit, yfit = fit_func(snr['LRG_SNR_MAG'][1], snr['LRG_FITRESULTS'])
lrg_fit.data['x'] = xfit
lrg_fit.data['logy'] = yfit
lrg_fit.data['y'] = 10**(yfit)
for key in ['fiber_id', 'ra', 'dec']:
    lrg_fit.data[key] = ['']*len(yfit)
#lrg_fit.stream(lrg_fit.data, 30)

xfit, yfit = fit_func(snr['QSO_SNR_MAG'][1], snr['QSO_FITRESULTS'])
qso_fit.data['x'] = xfit
qso_fit.data['logy'] = yfit
qso_fit.data['y'] = 10**(yfit)
for key in ['fiber_id', 'ra', 'dec']:
    qso_fit.data[key] = ['']*len(yfit)
#qso_fit.stream(qso_fit.data, 30)

xfit, yfit = fit_func(
    snr['STAR_SNR_MAG'][1], snr['STAR_FITRESULTS'])
star_fit.data['x'] = xfit
star_fit.data['logy'] = yfit
star_fit.data['y'] = 10**(yfit)
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

hover = HoverTool(tooltips=html_tooltip)
elg_plot = init_xy_plot(hover=hover)
elg_plot.line(x='x', y='y', source=elg_fit, color="black")
elg_plot.circle(x='x', y='y', source=elg, color="blue", size=8, line_color='black', alpha=0.7
            ,hover_color="blue", hover_alpha=1, hover_line_color='red')

elg_plot.xaxis.axis_label = "DECAM_R"
elg_plot.yaxis.axis_label = "SNR"
elg_plot.title.text = "ELG"

taptool = elg_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

hover = HoverTool(tooltips=html_tooltip)
lrg_plot = init_xy_plot(hover=hover)
lrg_plot.line(x='x', y='y', source=lrg_fit, color="black")
lrg_plot.circle(x='x', y='y', source=lrg, color="red", size=8, line_color='black', alpha=0.7
            , hover_color="red",hover_alpha=1, hover_line_color='red')

lrg_plot.xaxis.axis_label = "DECAM_R"
lrg_plot.yaxis.axis_label = "SNR"
lrg_plot.title.text = "LRG"

taptool = lrg_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

hover = HoverTool(tooltips=html_tooltip)
qso_plot = init_xy_plot(hover=hover)
qso_plot.line(x='x', y='y', source=qso_fit, color="black")
qso_plot.circle(x='x', y='y', source=qso, color="green", size=8, line_color='black', alpha=0.7
            ,hover_color="green", hover_alpha=1, hover_line_color='red')

qso_plot.xaxis.axis_label = "DECAM_R"
qso_plot.yaxis.axis_label = "SNR"
qso_plot.title.text = "QSO"

taptool = qso_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

hover = HoverTool(tooltips=html_tooltip)
star_plot = init_xy_plot(hover=hover)
star_plot.line(x='x', y='y', source=star_fit, color="black")
star_plot.circle(x='x', y='y', source=star, color="orange", size=8, line_color='black', alpha=0.7
            ,hover_color="orange", hover_alpha=1, hover_line_color='red')

star_plot.xaxis.axis_label = "DECAM_R"
star_plot.yaxis.axis_label = "SNR"
star_plot.title.text = "STAR"

taptool = star_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

plot = gridplot([[elg_plot, lrg_plot], [qso_plot, star_plot]], responsive=False)

# infos
key_name = 'snr'
info, nlines = write_info(key_name, tests[key_name])
txt = PreText(text=info, height=nlines*20)
# p2txt = column(widgetbox(txt),p2)
info_col = Div(text=write_description('snr'), width=2*star_plot.plot_width)
layout = column(widgetbox(info_col), plot)

curdoc().add_root(layout)
curdoc().title = "SNR"
