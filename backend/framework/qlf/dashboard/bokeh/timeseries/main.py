import numpy as np
import pandas as pd
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool, Legend
from bokeh.layouts import column

from bokeh.models.widgets import Div, Select, RangeSlider
from bokeh.resources import CDN
from bokeh.embed import file_html
import json
from bokeh.models import DatetimeTickFormatter
from log import get_logger
import os
from qlf_models import QLFModels
from datetime import datetime, timedelta
from astropy.time import Time

qlf_root = os.environ.get('QLF_ROOT')

logger = get_logger(
    "qlf.bokeh",
    os.path.join(qlf_root, "logs", "bokeh.log")
)


class TimeSeries():
    def __init__(self, yaxis, start, end, camera, amp=None):
        self.yaxis = yaxis
        self.start = datetime.strptime(start, '%Y%m%d').strftime('%Y-%m-%d')
        self.end = datetime.strptime(end, '%Y%m%d').strftime('%Y-%m-%d')
        self.camera = camera
        self.models = QLFModels()
        self.amp = amp

    def make_plot(self, outputs, objtype=None):
        colors = [
            'red',
            'blue',
            'green',
            'orange'
        ]
        legends=list()
        df = pd.DataFrame(list(outputs))
        if self.amp != None:
            for amp in self.amp.split(','):
                idx = int(amp)-1
                source = ColumnDataSource(data=dict(
                    x=df['mjd'],
                    y=df['value'].apply(lambda x: x[idx]),
                    exposure=df['exposure_id'],
                    camera=df['camera'],
                    dateobs=df['datef']
                ))
                line=self.p.line('x', 'y', source=source, line_color=colors[idx])
                circle=self.p.circle('x', 'y', source=source, size=6, line_color=None, fill_color=colors[idx])
                legends.append(('AMP {}'.format(idx+1), [line, circle]))
            legend = Legend(items=legends, location=(0, 0))
            self.p.add_layout(legend, 'below')
        else:
            source = ColumnDataSource(data=dict(
                x=df['mjd'],
                y=df['value'].apply(lambda x: x[0]),
                exposure=df['exposure_id'],
                camera=df['camera'],
                dateobs=df['datef']
            ))
        
            self.p.line('x', 'y', source=source)
            self.p.circle('x', 'y', source=source, size=5)

    def render(self):
        metrics_path = os.path.join(
            qlf_root, "framework", "ql_mapping",
            "metrics.json")

        with open(metrics_path) as f:
            metrics = json.load(f)
        axis_data = metrics[self.yaxis]
        outputs = self.models.get_product_metrics_by_camera(
            self.yaxis, self.camera, begin_date=self.start, end_date=self.end)

        TOOLTIPS = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">{}: </span>
                    <span style="font-size: 1vw; color: #515151;">@y</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Exposure: </span>
                    <span style="font-size: 1vw; color: #515151;">@exposure</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Date: </span>
                    <span style="font-size: 1vw; color: #515151;">@dateobs</span>
                </div>
            </div>
        """.format(axis_data['display'])

        hover = HoverTool(tooltips=TOOLTIPS)

        self.p = figure(
            title="Camera: {}".format(self.camera),
            sizing_mode='scale_width',
            toolbar_location='above',
            # x_axis_type="datetime",
            x_axis_label='Date (mjd)',
            y_axis_label=axis_data['display'],
            plot_width=700, plot_height=300,
            active_drag="box_zoom",
            tools=[hover, 'box_zoom,wheel_zoom,pan,reset']
        )

        font_size = "1.2vw"
        self.p.xaxis.major_label_text_font_size = font_size
        self.p.yaxis.major_label_text_font_size = font_size
        self.p.xaxis.axis_label_text_font_size = font_size
        self.p.yaxis.axis_label_text_font_size = font_size
        self.p.legend.label_text_font_size = font_size
        self.p.title.text_font_size = font_size

        self.make_plot(outputs)
        return file_html(self.p, CDN, "Time Series")
