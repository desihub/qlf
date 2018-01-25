from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource, Slider, CheckboxGroup, RadioButtonGroup, Div, LabelSet,\
    OpenURL, TapTool, HoverTool

from bokeh.plotting import curdoc, figure
from bokeh.charts.utils import df_from_json
from bokeh.charts import Donut

from dashboard.bokeh.helper import get_exposures, get_cameras
import pandas as pd

# Get the list of exposures
exposures = get_exposures()

expid = None

if exposures['expid']:
    exposures['expid'] = sorted(exposures['expid'])

    # By default display the last one on the interface
    expid = exposures['expid'][-1]
    flavor = exposures['flavor'][-1]

    # Page title reflects the selected exposure
    title = Div(text="<h3>Exposure ID {} ({})</h3>".format(expid, flavor))

    # Here we configure a 'slider' to change the exposure
    slider = Slider(start=exposures['expid'][0], end=expid,
                    value=expid, step=1, title="EXPOSURE ID")

# Now we configure the camera grid layout

# We need a 'hover' tool for each camera, these are things
# displayed when we hover on each camera

# Should we display scalars for all selected metrics? median values
# by camera or by each amplifier?

hover = HoverTool(tooltips=[("Camera", "@camera"), ("Status", "@status")])

# We have a fixed layout for the grid plot
# and we add the hover and the tap tool

# The tap tool will be used to click or 'tap' on the cameras and
# open the drill down plots associated to the selected metric

p = figure(x_range=(-1, 10), y_range=(0.5, 3.9), tools=[hover, 'tap'])
p.logo = None
p.toolbar_location = None

# Now we configure the camera column data source, each element of the column datasource
# represents a camera (30 cameras in total for the 10 spectrographs and 3 arms)

# The grid layout is the following, one row for each arm [b, r, z] and one column for
# each spectrograph [0, ...,9]

# Note: bokeh column data source elements must have the same length,
# thus some redundancy is expected here

# Mostly empty, this will be filled by the slider_update() and metric_update() functions

source = ColumnDataSource(data={
    "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] * 3, # positions of each camera
    "y": [1] * 10 + [2] * 10 + [3] * 10,
    "color": ["gray"] * 30, # they are gray by default
    "spectrograph": [None] * 30,  # spectrograph of each camera
    "arm": [None] * 30, # arm of each camera
    "expid": [None] * 30, # selected expid  (needed here?)
    "status": ["Not processed"] * 30,
    "camera": [None] * 30
})

camera_grid = p.square('x', 'y', color='color', size=45, source=source)

# Configure camera labels
# TODO: we can improve this

labels = ColumnDataSource(data={"x": [-0.9, -0.9, -0.9, -0.15, 0.85, 1.85, 2.85, 3.85, 4.85, 5.85, 6.85, 7.85, 8.85],
                                "y": [2.9, 1.9, 0.9] + [3.5]*10,
                                "text": ['b', 'r', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']})

label_set = LabelSet(x='x', y='y', text='text', source=labels, render_mode='canvas')


# Add labels to the plot layout
p.add_layout(label_set)

# Update the datasource when the selected exposure changes

def update(expid):

    # look up exposure properties
    index = exposures['expid'].index(expid)
    flavor = exposures['flavor'][index]

    title.text = "<h3>Exposure ID {} ({})</h3>".format(expid, flavor)

    # Get cameras registered in the DB for the selected exposure

    cameras = get_cameras()

    # Fill up the datasource with properties of each camera

    for camera in cameras:
        arm = camera['arm']
        spectrograph = int(camera['spectrograph'])

        if arm == 'b':
            source.data['color'][spectrograph+20] = "green"
            source.data['camera'][spectrograph+20] = camera['camera']
            source.data['status'][spectrograph+20] = "SNR passed"
            source.data['spectrograph'][spectrograph+20] = spectrograph
            source.data['arm'][spectrograph+20] = arm

        if arm == 'r':
            source.data['color'][spectrograph+10] = "green"
            source.data['camera'][spectrograph+10] = camera['camera']
            source.data['status'][spectrograph+10] = "SNR passed"
            source.data['spectrograph'][spectrograph+10] = spectrograph
            source.data['arm'][spectrograph+10] = arm

        if arm == 'z':
            source.data['color'][spectrograph] = "green"
            source.data['camera'][spectrograph] = camera['camera']
            source.data['status'][spectrograph] = "SNR passed"
            source.data['spectrograph'][spectrograph] = spectrograph
            source.data['arm'][spectrograph] = arm

    source.stream(source.data, 30)

if expid:
    # Update camera grid with data from the last exposure
    update(expid)

# Here we configure the tap tool to open the drill down plots for the selected camera and metric

# TODO: for now it is fixed for the SNR metric which will open the SNR vs. Mag plot

url = "/dashboard/qasnr?exposure={}&arm=@arm&spectrograph=@spectrograph".format(expid)

taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

# Configure an action if slider changes

def slider_update(attr, old, new):
    update(new)

slider.on_change('value', slider_update)

# Configure the metric selection

# TODO: this is fixed for now, we displaying the SNR metric only

metrics = ["COUNTS", "BIAS", "RMS", "XWSIGMA",
           "SKYCOUNTS", "SKYPEAK", "SNR"]

metric_select = CheckboxGroup(labels=metrics, active=[6], inline=False, width=50)

wedge_metric_select = RadioButtonGroup(
    labels=[ metrics[metric] for metric in metric_select.active], active=0)


def wedge_update(attr, old, new):

    wedge_metric_select.labels = [ metrics[metric] for metric in new ]


metric_select.on_change('active', wedge_update)


# Wedge plots (layout)

wedge = {'data': [{'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1 }]}

df = df_from_json(wedge)
df = pd.melt(df,
             value_vars=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
             value_name='number', var_name='spectrograph')

wedge_b = Donut(df, plot_height=220, plot_width=220, color=source.data['color'])
wedge_r = Donut(df, plot_height=220, plot_width=220, color=source.data['color'])
wedge_z = Donut(df, plot_height=220, plot_width=220, color=source.data['color'])

wedge_b.logo = None
wedge_r.logo = None
wedge_z.logo = None

wedge_b.toolbar_location = None
wedge_r.toolbar_location = None
wedge_z.toolbar_location = None

curdoc().add_root(row(widgetbox(title, width=700)))

curdoc().add_root(row(widgetbox(slider, width=700)))

curdoc().add_root(row(column(widgetbox(Div(text="<b>Cameras:</b>")),
                      p,
                      row(widgetbox(Div(text=""), width=50),
                          widgetbox(wedge_metric_select, width=600))),
                      column(widgetbox(Div(text="<b>Metrics:</b>"), width=150),
                             widgetbox(metric_select, width=150))))

curdoc().add_root(row(wedge_b, wedge_r, wedge_z))

curdoc().title = "Exposures"
