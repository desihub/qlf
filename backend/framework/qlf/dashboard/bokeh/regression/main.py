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


class Regression():
    def __init__(self, xaxis, yaxis, start, end, camera):
        self.yaxis = yaxis
        self.xaxis = xaxis
        self.start = datetime.strptime(start, '%Y%m%d').strftime('%Y-%m-%d')
        self.end = datetime.strptime(end, '%Y%m%d').strftime('%Y-%m-%d')
        self.camera = camera
        self.models = QLFModels()

    def render_plot(self, outputs_x, outputs_y):
        metrics_path = os.path.join(
            qlf_root, "framework", "ql_mapping",
            "metrics.json")

        with open(metrics_path) as f:
            metrics = json.load(f)
        y_data = metrics[self.yaxis]
        x_data = metrics[self.xaxis]
        df_x = pd.DataFrame(list(outputs_x))
        df_y = pd.DataFrame(list(outputs_y))
        source = ColumnDataSource(data=dict(
            x=df_x['value'].apply(lambda x: x[0]),
            y=df_y['value'].apply(lambda x: x[0]),
            exposure=df_x['exposure_id'],
            camera=df_x['camera']
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
        outputs_y = self.models.get_product_metrics_by_camera(
            self.yaxis, self.camera, begin_date=self.start, end_date=self.end)
        outputs_x = self.models.get_product_metrics_by_camera(
            self.xaxis, self.camera, begin_date=self.start, end_date=self.end)

        self.render_plot(outputs_x, outputs_y)

        return file_html(self.layout, CDN, "Regression")
