import os

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import row, column, widgetbox, gridplot

from dashboard.bokeh.helper import get_data, get_exposures, \
    init_xy_plot, get_url_args

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

# Get url query args
args = get_url_args(curdoc, defaults={'exposure': '3'})

selected_exposure = args['exposure']
selected_arm = args['arm']
selected_spectrograph = args['spectrograph']

exp_zfill = str(selected_exposure).zfill(8)

# get the data
qasnr = 'ql-snr-{}-{}.yaml'.format(selected_arm + selected_spectrograph, exp_zfill)

data = get_data(name=qasnr)

if data.empty:
    raise ValueError("No data to display, resquest from {}/qa".format(QLF_API_URL))

# create the bokeh column data sources
elg = ColumnDataSource(data={'x': data.ELG_SNR_MAG[1],
                             'y': data.ELG_SNR_MAG[0],
                             'fiber_id': data.ELG_FIBERID.dropna().tolist()})

# TODO: RA, Dec coordinates should come from the QA outputs

lrg = ColumnDataSource(data={'x': data.LRG_SNR_MAG[1],
                             'y': data.LRG_SNR_MAG[0],
                             'fiber_id': data.LRG_FIBERID.dropna().tolist(),
                             'ra': ["181.2035"] * len(data.LRG_SNR_MAG[1]),
                             'dec': ["-2.7371"] * len(data.LRG_SNR_MAG[1])})

qso = ColumnDataSource(data={'x': data.QSO_SNR_MAG[1],
                             'y': data.QSO_SNR_MAG[0],
                             'fiber_id': data.QSO_FIBERID.dropna().tolist()})

star = ColumnDataSource(data={'x': data.STAR_SNR_MAG[1],
                              'y': data.STAR_SNR_MAG[0],
                              'fiber_id': data.STAR_FIBERID.dropna().tolist()})

# make the app layout

# configure bokeh widgets
exposure = get_exposures()
slider = Slider(start=exposure['expid'][0], end=exposure['expid'][-1], value=int(selected_exposure), step=1,
                             title="Exposure ID")

# we can filter by spectrograph
spectrograph = Select(title="Spectrograph:",
                      value=selected_spectrograph,
                      options=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                      width=100)

# and arm
arm = Select(title="Arm:",
             value=selected_arm,
             options=['b', 'r', 'z'],
             width=100)

# here we make the plots

# hover = HoverTool(tooltips=[("Fiber ID", "@fiber_id"),
#                             ("Value", "@y")])

hover = HoverTool( tooltips="""
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Fiber ID: </span>
            <span style="font-size: 13px; color: #515151;">@fiber_id</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Value: </span>
            <span style="font-size: 13px; color: #515151;">@y</span>
        </div>
    </div>
    """
)

elg_plot = init_xy_plot(hover=hover)

elg_plot.circle(x='x', y='y', source=elg,
                color="blue", size=5)

elg_plot.xaxis.axis_label = "DECAM_R"
elg_plot.yaxis.axis_label = "SNR"
elg_plot.title.text = "ELG"

# hover = HoverTool(tooltips=[("SNR", "@y"),
#                             ("DECAM_R", "@x"),
#                             ("Fiber ID", "@fiber_id"),
#                             ("RA", "@ra"),
#                             ("Dec", "@dec")])

hover = HoverTool(tooltips="""
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
)

lrg_plot = init_xy_plot(hover=hover)

lrg_plot.circle(x='x', y='y', source=lrg,
                color="red", size=5)

lrg_plot.xaxis.axis_label = "DECAM_R"
lrg_plot.yaxis.axis_label = "SNR"
lrg_plot.title.text = "LRG"

url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr3"

taptool = lrg_plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

# hover = HoverTool(tooltips=[("Fiber ID", "@fiber_id"),
#                             ("Value", "@y")])

hover = HoverTool( tooltips="""
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Fiber ID: </span>
            <span style="font-size: 13px; color: #515151;">@fiber_id</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Value: </span>
            <span style="font-size: 13px; color: #515151;">@y</span>
        </div>
    </div>
    """
)

qso_plot = init_xy_plot(hover=hover)

qso_plot.circle(x='x', y='y', source=qso,
                color="green", size=5)

qso_plot.xaxis.axis_label = "DECAM_R"
qso_plot.yaxis.axis_label = "SNR"
qso_plot.title.text = "QSO"

# hover = HoverTool(tooltips=[("Fiber ID", "@fiber_id"),
#                             ("Value", "@y")])

hover = HoverTool( tooltips="""
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Fiber ID: </span>
            <span style="font-size: 13px; color: #515151;">@fiber_id</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Value: </span>
            <span style="font-size: 13px; color: #515151;">@y</span>
        </div>
    </div>
    """
)

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
