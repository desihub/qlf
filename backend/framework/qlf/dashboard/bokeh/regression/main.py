import numpy as np
import pandas as pd
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool, Legend, Spacer
from bokeh.layouts import gridplot

from bokeh.models.widgets import Div, Select, RangeSlider
from bokeh.resources import CDN
from bokeh.embed import file_html
import json
from bokeh.models import DatetimeTickFormatter
from log import get_logger
import os
from qlf_models import QLFModels
from datetime import datetime, timedelta

qlf_root = os.environ.get('QLF_ROOT')

logger = get_logger(
    "qlf.bokeh",
    os.path.join(qlf_root, "logs", "bokeh.log")
)

plots = {
    'skybrightness': {
        'display': 'SKY BRIGHTNESS',
        'path': 'TASKS->CHECK_SPECTRA->METRICS->PEAKCOUNT'
    },
    'airmass': {
        'display': 'AIRMASS',
        'path': 'GENERAL_INFO->AIRMASS'
    },
}

class Regression():
    def __init__(self, xaxis, yaxis, start, end, camera):
        self.yaxis = yaxis
        self.xaxis = xaxis
        self.start = datetime.strptime(start, '%Y%m%d').strftime('%Y-%m-%d')
        self.end = datetime.strptime(end, '%Y%m%d').strftime('%Y-%m-%d')
        self.camera = camera
        self.models = QLFModels()

    def render_plot(self, exposures, x_values, y_values, cameras):
        y_data = plots[self.yaxis]
        x_data = plots[self.xaxis]
        source = ColumnDataSource(data=dict(
            x=x_values,
            y=y_values,
            exposure=exposures,
            camera=cameras
        ))

        TOOLTIPS = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">{}: </span>
                    <span style="font-size: 1vw; color: #515151">@y</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">{}: </span>
                    <span style="font-size: 1vw; color: #515151;">@x</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Exposure: </span>
                    <span style="font-size: 1vw; color: #515151;">@exposure</span>
                </div>
            </div>
        """.format(y_data['display'], x_data['display'])

        hover = HoverTool(tooltips=TOOLTIPS)

        plot = figure(toolbar_location='above',
                      active_drag="box_zoom",
                      plot_height=300,
                    #   plot_width=500,
                      x_axis_label=x_data['display'],
                      y_axis_label=y_data['display'],
                      tools=[hover, 'box_zoom,pan,wheel_zoom,box_select,reset'])

        q = plot.circle('x', 'y', source=source, size=8,
                        fill_color='dodgerblue',
                        hover_fill_color='blue', line_color='black')

        hhist, hedges = np.histogram(source.data['x'], bins='sqrt')
        hmax = max(hhist)*1.1

        ph = figure(active_drag='box_zoom',
                    tools='box_zoom,pan,wheel_zoom,reset',
                    plot_height=250,
                    toolbar_location='left',
                    x_range=plot.x_range,
                    y_range=(-0.1*hmax, hmax),
                    y_axis_location="right",
                    min_border=10, min_border_left=50)

        ph.xgrid.grid_line_color = None
        ph.yaxis.major_label_orientation = 0

        qh = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:],
                     top=hhist, color="#a7bae1", line_color="black")

        # create the vertical histogram
        vhist, vedges = np.histogram(source.data['y'], bins='sqrt')
        vzeros = np.zeros(len(vedges)-1)
        vmax = max(vhist)*1.1

        pv = figure(active_drag='box_zoom',
                    tools='box_zoom,pan,wheel_zoom,reset',
                    toolbar_location='above',
                    plot_height=310,
                    y_range=plot.y_range,
                    x_range=(-0.1*vmax, vmax),
                    min_border=10, min_border_left=50)
        pv.ygrid.grid_line_color = None
        pv.xaxis.major_label_orientation = -np.pi/2
        pv.background_fill_color = "#fafafa"

        qv = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:],
                     right=vhist, color="#a7bae1", line_color="black")

        font_size = "1.2vw"
        for p in [plot, pv, ph]:
            p.xaxis.major_label_text_font_size = font_size
            p.yaxis.major_label_text_font_size = font_size
            p.xaxis.axis_label_text_font_size = font_size
            p.yaxis.axis_label_text_font_size = font_size
            p.legend.label_text_font_size = font_size
            p.title.text_font_size = font_size

        info = "<h3>Camera: {}<h3>".format(self.camera)
        info_col = Div(text=info)
        self.layout = gridplot([[info_col, None],
                                [plot, pv],
                                [ph, None]], sizing_mode='scale_width')

    def render(self):
        y_data = plots[self.yaxis]
        outputs_y = self.models.get_outputs_json_chunk_by_camera(
            y_data['path'], self.camera, begin_date=self.start, end_date=self.end)
        x_data = plots[self.xaxis]
        outputs_x = self.models.get_outputs_json_chunk_by_camera(
            x_data['path'], self.camera, begin_date=self.start, end_date=self.end)

        cameras = list()
        x_values = list()
        y_values = list()
        exposures = list()
        for idx, val in enumerate(outputs_y):
            if val['value']:
                exposures.append(val['exposure_id'])
                cameras.append(self.camera)
                y_values.append(val['value'])

        for idx, val in enumerate(outputs_x):
            if val['value']:
                x_values.append(val['value'])

        self.render_plot(exposures, x_values, y_values, cameras)

        return file_html(self.layout, CDN, "Regression")
