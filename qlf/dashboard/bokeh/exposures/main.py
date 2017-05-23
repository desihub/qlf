import os
import pandas as pd
from functools import partial
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, Slider, Select, RadioGroup, Button, Div, Label, LabelSet, OpenURL, TapTool, \
    Legend, CustomJS, Slider, HoverTool
from bokeh.plotting import curdoc, figure
from bokeh.charts.utils import df_from_json
from bokeh.charts import Donut

from dashboard.bokeh.helper import get_data, get_exposure_info, get_camera_info, init_xy_plot, get_camera_by_exposure, \
    get_all_exposure, get_all_camera, get_all_qa

# expid = 6

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

# AF: Column datasource to configure the labels

# AF: TODO: this could be a dict

sourcelabel = ColumnDataSource(data=dict(height=[0.9, 1.8, 2.7, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5],
                                    weight=[-0.9, -0.9, -0.9, -0.15, 0.85, 1.85, 2.85, 3.85, 4.85, 5.85, 6.85, 7.85,
                                            8.85],
                                    names=['z', 'r', 'b', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']))
hover = HoverTool(
    tooltips=[
        ("Camera", "@camera"),
        ("SNR", "")
    ]
)

# AF: Fix plot range to display the grid

p = figure(x_range=(-2, 11), y_range=(0.5, 3.9), tools=[hover, 'tap'])

labels = LabelSet(x='weight', y='height', text='names', x_offset=5, y_offset=5, source=sourcelabel, render_mode='canvas')

# AF: Move this to theme.yaml which define the plot style

p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.add_layout(labels)
color_listr = list()
color_listz = list()
color_listg = list()
for i in range(30):
    color_listr.append('#A9A9A9')
    color_listz.append('#A9A9A9')
    color_listg.append('#A9A9A9')

# start with an empty datasource and populate the properties of each camera
source = ColumnDataSource(data=dict(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    y=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    color=color_listr,
    # name = list(),
    spectrograph=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    arm=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    exposure=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    camera=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
))
exposurePos = 0
def update(btn):
    # based on the QA results available in the database for that exposure.
    global exposurePos
    exposure_list = list()
    exposures = get_all_exposure()
    for exposure in exposures:
        exposure_list.append(exposure['expid'])

    if exposurePos > 0 and btn == 'prev':
        exposurePos -= 1

    if exposurePos < len(exposure_list) -1 and btn == 'next':
        exposurePos += 1
    expid = int(exposure_list[exposurePos])
    cam = get_camera_by_exposure(expid)
    title.text = '<h3>Exposure ID %s (%s)</h3>' % (expid, flavor)
    # AF: the only thing that changes is the y coord in each datasource
    new_data = data=dict(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        y=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        color=color_listr,
        # name = list(),
        spectrograph=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        arm=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        exposure=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        camera=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )
    for i in cam:
        if i['arm'] == 'r':
            pos = int(i['spectrograph'])
            new_data['color'][pos] = '#32CD32'
            new_data['y'][pos] = 2
            new_data['spectrograph'][pos] = i['spectrograph']
            new_data['arm'][pos] = i['arm']
            new_data['exposure'][pos] = expid
            new_data['camera'][pos] = i['camera']

        if i['arm'] == 'b':
            pos = int(i['spectrograph'])
            new_data['color'][pos] = '#32CD32'
            new_data['y'][pos] = 3
            new_data['spectrograph'][pos] = i['spectrograph']
            new_data['arm'][pos] = i['arm']
            new_data['exposure'][pos] = expid
            new_data['camera'][pos] = i['camera']

        if i['arm'] == 'z':
            pos = int(i['spectrograph'])
            new_data['color'][pos] = '#32CD32'
            new_data['y'][pos] = 1
            new_data['spectrograph'][pos] = i['spectrograph']
            new_data['arm'][pos] = i['arm']
            new_data['exposure'][pos] = expid
            new_data['camera'][pos] = i['camera']

        source.stream(new_data,30)


p.square('x', 'y', color='color', name='name', size=50, source=source)

exp_info = dict()
exp_info['telra'] = None
exp_info['teldec'] = None
exp_info['airmass'] = None
exp_info['exptime'] = None
flavor = 'object'
title = Div(text='<h3>Exposure ID %s (%s)</h3>' % (0, flavor))

board = Div(text='''
    <div
        style="border-radius:
        25px; background:
        #DCDCDC;
        width: 160px;
        padding: 20px;"
    >
    <b>RA:</b> %s <br />
    <b>Dec:</b> %s <br />
    <b>Airmass:</b> %s <br />
    <b>Exposure Time:</b> %s <br />
    <b>ETC predicted SNR:</b> None <br />
    <b>Measured SNR:</b> None <br />
    </div>''' % (
    exp_info['telra'],
    exp_info['teldec'],
    exp_info['airmass'],
    exp_info['exptime'],
),
            width=160
            )

buttonp = Button(label="<< Previous")  # , callback=callback)
buttonn = Button(label="Next >>")  # , callback=callbackn)

buttonn.on_click(partial(update, btn='next'))
buttonp.on_click(partial(update, btn='prev'))

update('next')


# AF: Should route to django instead
url = "http://localhost:8000/dashboard/qasnr?exposure=@exposure&arm=@arm&spectrograph=@spectrograph"
taptool = p.select(type=TapTool)

# AF: Is there another way to add link to hover tooltips?
taptool.callback = OpenURL(url=url)

# AF: Radio group for QA's
radio = RadioGroup(labels=['COUNTPIX', 'GETBIAS', 'GETRMS', 'XWSIGMA', 'COUNTBINS', 'INTEG', 'SKYCOUNT', 'SKYPEAK', 'SNR'],
                   active=8, inline=False, width=50)

# AF: Define app Layout in one command ?

curdoc().add_root(row(buttonp, title, buttonn))

curdoc().add_root(row(widgetbox(radio, width=160), gridplot([[p]], toolbar_location=None, plot_width=800)))
curdoc().title = "Exposures"
