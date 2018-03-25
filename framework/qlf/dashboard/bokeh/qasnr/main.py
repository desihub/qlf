import os
import sys

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models.widgets import PreText
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.helper import write_info


from dashboard.bokeh.helper import get_data, get_exposure_ids, \
    init_xy_plot, get_url_args, get_arms_and_spectrographs
import numpy as np


QLF_API_URL = os.environ.get(
    'QLF_API_URL',
    'http://localhost:8000/dashboard/api'
)

# Get url query args
args = get_url_args(curdoc)

selected_exposure = args['exposure']
selected_arm = args['arm']
selected_spectrograph = args['spectrograph']

#load from scalar_metrics
from dashboard.bokeh.utils.scalar_metrics import LoadMetrics
night = '20190101'

cam = selected_arm+str(selected_spectrograph)
exp = selected_exposure 
lm = LoadMetrics(cam, exp, night);
metrics, tests  = lm.metrics, lm.tests 


def fit_func(xdata, coeff):
    a, b, c = coeff[0]
    x = np.linspace( min(xdata), max(xdata), 1000)
    
    y = a + b*x + c*x**2
    return x, y
    

data_model = {
    'x': [],
    'y': [],
    'logy':[],
    'fiber_id': [],
    'ra': [],
    'dec': []
}

elg = ColumnDataSource(data=data_model.copy())
lrg = ColumnDataSource(data=data_model.copy())
qso = ColumnDataSource(data=data_model.copy())
star = ColumnDataSource(data=data_model.copy())


params = [
    'ELG_SNR_MAG', 'ELG_FIBERID',
    'LRG_SNR_MAG', 'LRG_FIBERID',
    'QSO_SNR_MAG', 'QSO_FIBERID',
    'STAR_SNR_MAG', 'STAR_FIBERID',
    'RA', 'DEC'
]


data_fit = {
    'x': [],
    'y': [],
    'logy':[],
    'fiber_id': [],
    'ra': [],
    'dec': []
}
elg_fit = ColumnDataSource(data = data_fit.copy() )
lrg_fit = ColumnDataSource(data = data_fit.copy() )
qso_fit = ColumnDataSource(data = data_fit.copy() )
star_fit = ColumnDataSource(data = data_fit.copy() )
params_fit = ['ELG_FITRESULTS', 'LRG_FITRESULTS', 'QSO_FITRESULTS', 'STAR_FITRESULTS']


def update(arm, spectrograph, exposure_id):
    exp_zfill = str(exposure_id).zfill(8)

    # get the data
    qa_snr = 'ql-snr-{}-{}.yaml'.format(arm + spectrograph, exp_zfill)
    try:
        data = get_data(qa_snr, params)
    except:
        sys.exit('Could not load snr metrics')


    if not data.empty:
        # drop rows that have ELG_FIBERID null
        elg_data = data[data.ELG_FIBERID.notnull()]

        # create the bokeh column data sources
        elg.data['x'] = elg_data.ELG_SNR_MAG[1]
        elg.data['y'] = elg_data.ELG_SNR_MAG[0]
        elg.data['logy'] = np.log10(np.array( elg_data.ELG_SNR_MAG[0]))
        elg.data['fiber_id'] = elg_data.ELG_FIBERID.tolist()
        elg.data['ra'] = elg_data.RA.tolist()
        elg.data['dec'] = elg_data.DEC.tolist()
        ## elg.stream(elg.data, 30)

        # drop rows that have ELG_FIBERID null
        lrg_data = data[data.LRG_FIBERID.notnull()]

        lrg.data['x'] = lrg_data.LRG_SNR_MAG[1]
        lrg.data['y'] = lrg_data.LRG_SNR_MAG[0]
        lrg.data['logy'] = np.log10(np.array( lrg_data.LRG_SNR_MAG[0]))
        lrg.data['fiber_id'] = lrg_data.LRG_FIBERID.dropna().tolist()
        lrg.data['ra'] = lrg_data.RA.dropna().tolist()
        lrg.data['dec'] = lrg_data.DEC.dropna().tolist()
        ## lrg.stream(lrg.data, 30)

        # drop rows that have QSO_FIBERID null
        qso_data = data[data.QSO_FIBERID.notnull()]

        qso.data['x'] = qso_data.QSO_SNR_MAG[1]
        qso.data['y'] = qso_data.QSO_SNR_MAG[0]
        qso.data['logy'] = np.log10(np.array( qso_data.QSO_SNR_MAG[0]))
        qso.data['fiber_id'] = qso_data.QSO_FIBERID.dropna().tolist()
        qso.data['ra'] = qso_data.RA.dropna().tolist()
        qso.data['dec'] = qso_data.DEC.dropna().tolist()
        ## qso.stream(qso.data, 30)

        # drop rows that have STAR_FIBERID null
        star_data = data[data.STAR_FIBERID.notnull()]

        star.data['x'] = star_data.STAR_SNR_MAG[1]
        star.data['y'] = star_data.STAR_SNR_MAG[0]
        star.data['logy'] = np.log10(np.array( star_data.STAR_SNR_MAG[0]))
        star.data['fiber_id'] = star_data.STAR_FIBERID.dropna().tolist()
        star.data['ra'] = star_data.RA.dropna().tolist()
        star.data['dec'] = star_data.DEC.dropna().tolist()
        ## star.stream(star.data, 30)

    # fitting function
    data2 = get_data(qa_snr, params_fit)
    if not data2.empty:

        xfit, yfit = fit_func(elg_data.ELG_SNR_MAG[1], data2['ELG_FITRESULTS'])
        elg_fit.data['x'] = xfit 
        elg_fit.data['logy'] = yfit 
        elg_fit.data['y'] = 10**(yfit) 
        for key in ['fiber_id', 'ra', 'dec']:
            elg_fit.data[key] = ['']*len(yfit) 
        #elg_fit.stream(elg_fit.data, 30)

        xfit, yfit = fit_func(lrg_data.LRG_SNR_MAG[1], data2['LRG_FITRESULTS'])
        lrg_fit.data['x'] = xfit 
        lrg_fit.data['logy'] = yfit 
        lrg_fit.data['y'] = 10**(yfit) 
        for key in ['fiber_id', 'ra', 'dec']:
            lrg_fit.data[key] = ['']*len(yfit) 
        #lrg_fit.stream(lrg_fit.data, 30)

        xfit, yfit = fit_func(qso_data.QSO_SNR_MAG[1], data2['QSO_FITRESULTS'])
        qso_fit.data['x'] = xfit 
        qso_fit.data['logy'] = yfit 
        qso_fit.data['y'] = 10**(yfit) 
        for key in ['fiber_id', 'ra', 'dec']:
            qso_fit.data[key] = ['']*len(yfit) 
        #qso_fit.stream(qso_fit.data, 30)

        xfit, yfit = fit_func(star_data.STAR_SNR_MAG[1], data2['STAR_FITRESULTS'])
        star_fit.data['x'] = xfit 
        star_fit.data['logy'] = yfit 
        star_fit.data['y'] = 10**(yfit) 
        for key in ['fiber_id', 'ra', 'dec']:
            star_fit.data[key] = ['']*len(yfit) 
        #star_fit.stream(star_fit.data, 30)

# configure bokeh widgets
# exposure = get_exposure_ids()

# if not exposure:
#     exposure.append(int(selected_exposure))

# exposure = sorted(exposure)

# exp_slider = Slider(
#     start=int(exposure[0]), end=int(exposure[-1]),
#     value=int(selected_exposure), step=1,
#     title="Exposure ID")

# cameras = get_arms_and_spectrographs()

# if not cameras["spectrographs"]:
#     cameras["spectrographs"].append(selected_spectrograph)

# if not cameras["arms"]:
#     cameras["arms"].append(selected_arm)

# # we can filter by spectrograph
# spectrograph_select = Select(
#     title="Spectrograph:",
#     value=selected_spectrograph,
#     options=cameras["spectrographs"],
#     width=100)

# # and arm
# arm_select = Select(
#     title="Arm:",
#     options=cameras['arms'],
#     value=selected_arm,
#     width=100)

# def arm_handler(attr, old, value):
#     update(value, spectrograph_select.value, exp_slider.value)

# def spectrograph_handler(attr, old, value):
#     update(arm_select.value, value, exp_slider.value)

# def exposure_handler(attr, old, value):
#     update(arm_select.value, spectrograph_select.value, value)

# arm_select.on_change("value", arm_handler)
# spectrograph_select.on_change("value", spectrograph_handler)
# exp_slider.on_change("value", exposure_handler)

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

update(selected_arm, selected_spectrograph, selected_exposure)

plot = gridplot([[elg_plot, lrg_plot], [qso_plot, star_plot]], responsive=True)

# and create the final layout
# layout = column(widgetbox(exp_slider, responsive=True),
#                 row(widgetbox(arm_select, width=130),
#                     widgetbox(spectrograph_select, width=130)),
#                 plot, responsive=True)



#infos
key_name = 'snr'
info, nlines = write_info(key_name, tests[key_name])
txt = PreText(text=info, height=nlines*20)
#p2txt = column(widgetbox(txt),p2)

layout = column(plot, responsive=True)

curdoc().add_root(layout)
curdoc().title = "SNR"
