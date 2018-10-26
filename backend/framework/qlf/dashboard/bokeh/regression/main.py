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

        plot = figure(title="Camera: {}".format(self.camera),
                      toolbar_location='above',
                      active_drag="box_zoom",
                      plot_height=300,
                    #   plot_width=500,
                      x_axis_label=x_data['display'],
                      y_axis_label=y_data['display'],
                      tools=[hover, 'box_zoom,pan,wheel_zoom,box_select,reset'],
                      sizing_mode='scale_width')

        q = plot.circle('x', 'y', source=source, size=8,
                        fill_color='dodgerblue',
                        hover_fill_color='blue', line_color='black')

        font_size = "1.2vw"
        plot.xaxis.major_label_text_font_size = font_size
        plot.yaxis.major_label_text_font_size = font_size
        plot.xaxis.axis_label_text_font_size = font_size
        plot.yaxis.axis_label_text_font_size = font_size
        plot.legend.label_text_font_size = font_size
        plot.title.text_font_size = font_size

        self.layout = plot

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
