import os

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import row, column, widgetbox, gridplot

from dashboard.bokeh.helper import get_data, get_exposure_info, get_camera_info, \
    init_xy_plot, get_url_args

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

# Get url query args
args = get_url_args(curdoc, defaults={'expid': '3'})

# get the data
data = get_data(name='ql-snr-z0-00000003.yaml')

if data.empty:
    raise ValueError("No data to display, resquest from {}/qa".format(QLF_API_URL))

# create the bokeh column data sources
elg = ColumnDataSource(data={'x': data.ELG_SNR_MAG[1],
                             'y': data.ELG_SNR_MAG[0],
                             'fiber_id': data.ELG_FIBERID.dropna().tolist()})

lrg = ColumnDataSource(data={'x': data.LRG_SNR_MAG[1],
                             'y': data.LRG_SNR_MAG[0],
                             'fiber_id': data.LRG_FIBERID.dropna().tolist()})

qso = ColumnDataSource(data={'x': data.QSO_SNR_MAG[1],
                             'y': data.QSO_SNR_MAG[0],
                             'fiber_id': data.QSO_FIBERID.dropna().tolist()})

star = ColumnDataSource(data={'x': data.STAR_SNR_MAG[1],
                              'y': data.STAR_SNR_MAG[0],
                              'fiber_id': data.STAR_FIBERID.dropna().tolist()})

# make the app layout

# configure bokeh widgets
exposure = get_exposure_info()
slider = Slider(start=exposure['expid'][0], end=exposure['expid'][-1], value=exposure['expid'][0], step=1,
                             title="Exposure ID")

# we can filter by spectrograph
camera = get_camera_info()
spectrograph = Select(title="Spectrograph:",
                      value=camera['spectrograph'][0],
                      options=camera['spectrograph'],
                      width=100)

# and arm
arm = Select(title="Arm:",
             value=camera['arm'][0],
             options=camera['arm'],
             width=100)

# here we make the plots
hover = HoverTool(tooltips=[("Fiber ID", "@fiber_id"),
                            ("Value", "@y")])

elg_plot = init_xy_plot(hover=hover)

elg_plot.circle(x='x', y='y', source=elg,
                color="blue", size=5)

elg_plot.xaxis.axis_label = "DECAM_R"
elg_plot.yaxis.axis_label = "SNR"
elg_plot.title.text = "ELG"

hover = HoverTool(tooltips=[("Fiber ID", "@fiber_id"),
                            ("Value", "@y")])

lrg_plot = init_xy_plot(hover=hover)

lrg_plot.circle(x='x', y='y', source=lrg,
                color="red", size=5)

lrg_plot.xaxis.axis_label = "DECAM_R"
lrg_plot.yaxis.axis_label = "SNR"
lrg_plot.title.text = "LRG"

hover = HoverTool(tooltips=[("Fiber ID", "@fiber_id"),
                            ("Value", "@y")])

qso_plot = init_xy_plot(hover=hover)

qso_plot.circle(x='x', y='y', source=qso,
                color="green", size=5)

qso_plot.xaxis.axis_label = "DECAM_R"
qso_plot.yaxis.axis_label = "SNR"
qso_plot.title.text = "QSO"

hover = HoverTool(tooltips=[("Fiber ID", "@fiber_id"),
                            ("Value", "@y")])

star_plot = init_xy_plot(hover=hover)
star_plot.circle(x='x', y='y', source=star,
                 color="black", size=5)

star_plot.xaxis.axis_label = "DECAM_R"
star_plot.yaxis.axis_label = "SNR"
star_plot.title.text = "STAR"

plot = gridplot([[elg_plot, lrg_plot], [qso_plot, star_plot]])

# and create the final layout
layout = column(widgetbox(slider, width=1000),
                row(widgetbox(arm, width=150),
                    widgetbox(spectrograph, width=150)),
                plot)


curdoc().add_root(layout)
curdoc().title = "SNR"


