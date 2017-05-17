import os
import pandas as pd

from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, Slider, Select, RadioGroup, Button, Div, Label, LabelSet, OpenURL, TapTool, \
    Legend, CustomJS, Slider, HoverTool
from bokeh.plotting import curdoc, figure
from bokeh.charts.utils import df_from_json
from bokeh.charts import Donut

from dashboard.bokeh.helper import get_data, get_exposure_info, get_camera_info, init_xy_plot, get_camera_by_exposure, \
    get_all_exposure, get_all_camera, get_all_qa

from bokeh import events

expid = 1

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

source = ColumnDataSource(data=dict(height=[0.9, 1.8, 2.7, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5],
                                    weight=[-0.9, -0.9, -0.9, -0.15, 0.85, 1.85, 2.85, 3.85, 4.85, 5.85, 6.85, 7.85,
                                            8.85],
                                    names=['z', 'r', 'g', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']))
hover = HoverTool(
    tooltips=[
        ("Camera", "(@camera)"),
    ]
)

p = figure(x_range=(-2, 11), y_range=(0.5, 3.9), tools=[hover, 'tap'])

labels = LabelSet(x='weight', y='height', text='names', x_offset=5, y_offset=5, source=source, render_mode='canvas')
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.add_layout(labels)
color_listr = list()
color_listz = list()
color_listg = list()
for i in range(10):
    color_listr.append('#A9A9A9')
    color_listz.append('#A9A9A9')
    color_listg.append('#A9A9A9')

sourcer = ColumnDataSource(data=dict(
    x=list(range(10)),
    y=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    color=color_listr,
    # name = list(),
    spectrograph=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    arm=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    exposure=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    camera=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
))
sourceg = ColumnDataSource(data=dict(
    x=list(range(10)),
    y=[3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    color=color_listg,
    # name = list(),
    spectrograph=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    arm=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    exposure=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    camera=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
))
sourcez = ColumnDataSource(data=dict(
    x=list(range(10)),
    y=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    color=color_listz,
    # name = list(),
    spectrograph=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    arm=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    exposure=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    camera=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
))
exp = get_all_exposure()
cam = get_camera_by_exposure(expid)
sourcecam = ColumnDataSource(data=dict(
    cam=cam,
    exp_list=list()
))
flavor = 0
for i in cam:
    if i['arm'] == 'r':
        pos = int(i['spectrograph'])
        sourcer.data['color'][pos] = '#32CD32'
        sourcer.data['spectrograph'][pos] = i['spectrograph']
        sourcer.data['arm'][pos] = i['arm']
        sourcer.data['exposure'][pos] = i['exposure']
        sourcer.data['camera'][pos] = i['camera']

    if i['arm'] == 'g':
        pos = int(i['spectrograph'])
        sourceg.data['color'][pos] = '#32CD32'
        sourceg.data['spectrograph'][pos] = i['spectrograph']
        sourceg.data['arm'][pos] = i['arm']
        sourceg.data['exposure'][pos] = i['exposure']
        sourcer.data['camera'][pos] = i['camera']

    if i['arm'] == 'z':
        pos = int(i['spectrograph'])
        sourcez.data['color'][pos] = '#32CD32'
        sourcez.data['spectrograph'][pos] = i['spectrograph']
        sourcez.data['arm'][pos] = i['arm']
        sourcez.data['exposure'][pos] = i['exposure']
        sourcer.data['camera'][pos] = i['camera']

p.square('x', 'y', color='color', name='name', size=50, source=sourcer)
p.square('x', 'y', color='color', name='name', size=50, source=sourceg)
p.square('x', 'y', color='color', name='name', size=50, source=sourcez)

for i in exp:
    i['expid'] = int(i['expid'])
exp_info = [d for d in exp if d['expid'] in [expid]][0]
flavor = exp_info['flavor']
title = Div(text='<h3>Exposure ID %s, flavor: %s</h3>' % (expid, flavor))
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

buttonp = Button(label="<< Previous")
buttonn = Button(label="Next >>")
url = "http://localhost:5006/qa-snr?exposure=@exposure&arm=@arm&spectrograph=@spectrograph"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)
# sourceurl = ColumnDataSource(data=dict(
#     url = [url]
# ))
# taptool.callback = CustomJS(args=dict(sourceurl=sourceurl), code="""
#     url = sourceurl.data['url'][0]
#     // window.open("http://foo.com" ,"_self");
#     window.open(url, "_blank", "toolbar=yes,scrollbars=yes,resizable=yes,top=500,left=500,width=500,height=500");
#     """)

list_qa = list()
qa = get_all_qa()
for i in qa:
    list_qa.append(i['display_name'])
radio = RadioGroup(labels=list_qa, active=len(list_qa) - 1, inline=False, width=100)

space = Div(text='<h3></h3>', width=60)

curdoc().add_root(row(space, buttonp, title, buttonn))
curdoc().add_root(row(gridplot([[p]], toolbar_location="right", plot_width=1000), column(radio, board)))


def callback(sourcez, sourcer, sourceg, title, sourcecam, exp_list):
    global cam
    cam = get_all_camera()
    sourcecam.data['cam'] = cam
    sourcecam.data['exp_list'] = exp_list
    return CustomJS(args=dict(
        sourcez=sourcez,
        sourcer=sourcer,
        sourceg=sourceg,
        title=title,
        sourcecam=sourcecam
    ), code="""
        exp_list = sourcecam.data['exp_list']
        cam = sourcecam.data['cam']
        expo = 0
        if (window.testando === undefined){
             (window.testando)
            window.testando = 0
        }
        if (window.testando < exp_list.length - 1){
            window.testando += 1
            expo = exp_list[window.testando]
            var cam = cam.filter(function(obj) { return obj.exposure == expo; });
            var dataz = sourcez.data;
            var datar = sourcer.data;
            var datag = sourceg.data;
            colorz = dataz['color']
            colorr = datar['color']
            colorg = datag['color']
            for (i = 0; i < 10; i++) {
                colorg[i] = '#A9A9A9'
                colorr[i] = '#A9A9A9'
                colorz[i] = '#A9A9A9'
            }
            for (i = 0; i < cam.length; i++) {
                if (cam[i].arm == 'r'){
                    pos = parseInt(cam[i].spectrograph)
                    sourcer.data['color'][pos] = '#32CD32'
                    sourcer.data['arm'][pos] = cam[i].arm
                    sourcer.data['exposure'][pos] = cam[i].exposure
                    sourcer.data['spectrograph'][pos]= cam[i].spectrograph
                    sourcer.data['camera'][pos]= cam[i].camera
                }

                if (cam[i].arm == 'z'){
                    pos = parseInt(cam[i].spectrograph)
                    sourcez.data['color'][pos] = '#32CD32'
                    sourcez.data['arm'][pos] = cam[i].arm
                    sourcez.data['exposure'][pos] = cam[i].exposure
                    sourcez.data['spectrograph'][pos]= cam[i].spectrograph
                    sourcez.data['camera'][pos]= cam[i].camera
                }

                if (cam[i].arm == 'g'){
                    pos = parseInt(cam[i].spectrograph)
                    sourceg.data['color'][pos] = '#32CD32'
                    sourceg.data['arm'][pos] = cam[i].arm
                    sourceg.data['exposure'][pos] = cam[i].exposure
                    sourceg.data['spectrograph'][pos]= cam[i].spectrograph
                    sourceg.data['camera'][pos]= cam[i].camera
                }
            }
            sourcer.trigger('change');
            sourceg.trigger('change');
            sourcez.trigger('change');
            title.text = '<h3>Exposure ID '+cam[0].exposure+', flavor: Object</h3>'
        }
         ('nx')
    """)


def callbackp(sourcez, sourcer, sourceg, title, sourcecam, exp_list):
    global cam
    cam = get_all_camera()
    sourcecam.data['cam'] = cam
    sourcecam.data['exp_list'] = exp_list
    return CustomJS(args=dict(
        sourcez=sourcez,
        sourcer=sourcer,
        sourceg=sourceg,
        title=title,
        sourcecam=sourcecam
    ), code="""
        exp_list = sourcecam.data['exp_list']
        cam = sourcecam.data['cam']
        expo = 0
        if (window.testando === undefined){
             (window.testando)
            window.testando = 0
        }
        if (window.testando > 0){
            window.testando -= 1
            expo = exp_list[window.testando]
            //  (exp_list)
            //  (expo)
            var cam = cam.filter(function(obj) { return obj.exposure == expo; });
            var dataz = sourcez.data;
            var datar = sourcer.data;
            var datag = sourceg.data;
            colorz = dataz['color']
            colorr = datar['color']
            colorg = datag['color']
            for (i = 0; i < 10; i++) {
                colorg[i] = '#A9A9A9'
                colorr[i] = '#A9A9A9'
                colorz[i] = '#A9A9A9'
            }
            for (i = 0; i < cam.length; i++) {
                if (cam[i].arm == 'r'){
                    pos = parseInt(cam[i].spectrograph)
                    sourcer.data['color'][pos] = '#32CD32'
                    sourcer.data['arm'][pos] = cam[i].arm
                    sourcer.data['exposure'][pos] = cam[i].exposure
                    sourcer.data['spectrograph'][pos]= cam[i].spectrograph
                    sourcer.data['camera'][pos]= cam[i].camera

                }

                if (cam[i].arm == 'z'){
                    pos = parseInt(cam[i].spectrograph)
                    sourcez.data['color'][pos] = '#32CD32'
                    sourcez.data['arm'][pos] = cam[i].arm
                    sourcez.data['exposure'][pos] = cam[i].exposure
                    sourcez.data['spectrograph'][pos]= cam[i].spectrograph
                    sourcez.data['camera'][pos]= cam[i].camera
                }

                if (cam[i].arm == 'g'){
                    pos = parseInt(cam[i].spectrograph)
                    sourceg.data['color'][pos] = '#32CD32'
                    sourceg.data['arm'][pos] = cam[i].arm
                    sourceg.data['exposure'][pos] = cam[i].exposure
                    sourceg.data['spectrograph'][pos]= cam[i].spectrograph
                    sourceg.data['camera'][pos]= cam[i].camera
                }
            }
            sourceg.trigger('change');
            sourcer.trigger('change');
            sourcez.trigger('change');
            title.text = '<h3>Exposure ID '+cam[0].exposure+', flavor: Object</h3>'
        }
         ('pr')
    """)


exp = get_all_exposure()
exp_list = list()
for i in range(len(exp)):
    val = i + 1
    exp_list.append(val)

buttonp.js_on_event(
    events.ButtonClick,
    callbackp(
        sourcez,
        sourcer,
        sourceg,
        title,
        sourcecam,
        exp_list
    )
)

buttonn.js_on_event(
    events.ButtonClick,
    callback(
        sourcez,
        sourcer,
        sourceg,
        title,
        sourcecam,
        exp_list
    )
)

data = {
    'data': [
        {
            '0': 1,
            '1': 1,
            '2': 1,
            '3': 1,
            '4': 1,
            '5': 1,
            '6': 1,
            '7': 1,
            '8': 1,
            '9': 1,
        }
    ]
}
df = df_from_json(data)
df = pd.melt(df,
             value_vars=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
             value_name='spectrograph_count', var_name='spectrograph')

sourcedz = ColumnDataSource(
    data=dict(height=[-1.6],
              weight=[-0.1],
              names=['z']))
sourcedr = ColumnDataSource(
    data=dict(height=[-1.6],
              weight=[-0.1],
              names=['r']))
sourcedg = ColumnDataSource(
    data=dict(height=[-1.6],
              weight=[-0.1],
              names=['g']))

labelr = LabelSet(x='weight', y='height', text='names', x_offset=5, y_offset=5, source=sourcedr, render_mode='canvas')
labelz = LabelSet(x='weight', y='height', text='names', x_offset=5, y_offset=5, source=sourcedz, render_mode='canvas')
labelg = LabelSet(x='weight', y='height', text='names', x_offset=5, y_offset=5, source=sourcedg, render_mode='canvas')
d = Donut(df, plot_height=280, plot_width=250, tools="tap", color=sourcer.data['color'], toolbar_location="left")
d.add_layout(labelg)
d2 = Donut(df, plot_height=280, plot_width=250, tools="tap", color=sourceg.data['color'], toolbar_location="left")
d2.add_layout(labelr)
d3 = Donut(df, plot_height=280, plot_width=250, tools="tap", color=sourcez.data['color'], toolbar_location="left")
d3.add_layout(labelz)
space = Div(text='<h3></h3>', width=120)
curdoc().add_root(row(space, d, d2, d3))
curdoc().title = "Exposures"