import holoviews as hv
import pandas as pd
import holoviews.plotting.bokeh
from qlf_models import QLFModels
from holoviews.operation.datashader import datashade
from bokeh.plotting import curdoc
import sys
from datetime import datetime

try:
    models = QLFModels()

    renderer = hv.renderer('bokeh')

    args = curdoc().session_context.request.arguments

    def get_arg_string(key):
        try:
            return args.get(key)[0].decode("utf-8")
        except:
            return None

    yaxis = get_arg_string('yaxis')
    xaxis = get_arg_string('xaxis')
    start_date = get_arg_string('start')
    start_date = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
    end_date = get_arg_string('end')
    end_date = datetime.strptime(end_date, '%Y%m%d').strftime('%Y-%m-%d')
    camera = get_arg_string('camera')

    outputs_y = models.get_product_metrics_by_camera(
        yaxis, camera, begin_date=start_date, end_date=end_date)
    outputs_x = models.get_product_metrics_by_camera(
        xaxis, camera, begin_date=start_date, end_date=end_date)

    df_y = pd.DataFrame(list(outputs_y))
    df_x = pd.DataFrame(list(outputs_x))

    plot = hv.Curve([])
    df_x[yaxis] = df_y['value'].apply(lambda x: x[0])
    df_x[xaxis] = df_x['value'].apply(lambda x: x[0])
    plot = hv.Points(df_x, [xaxis, yaxis], ['exposure_id', 'camera',
                            'datef', 'dateobs'])
    layout = plot.redim.label(x=xaxis, y=yaxis).opts(
        sizing_mode='scale_width', height=150, padding=0.1, fontsize='1.2vw', toolbar='above', active_tools=["box_zoom"], title='Camera: {}'.format(camera))
    doc = renderer.server_doc(layout)
    doc.title = 'Time Series'
except Exception as e:
    renderer = hv.renderer('bokeh')
    print('error', e)
    doc = renderer.server_doc(hv.Div("""
        <p style="font-size: 2.2vw"> Couldn't Load Regression </p>
    """))
    doc.title = 'Regression Error'
