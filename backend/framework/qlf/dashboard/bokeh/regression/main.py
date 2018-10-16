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
        data_model = dict(
            noise1=noise[0], noise2=noise[1], noise3=noise[2], noise4=noise[3],
            bias1=bias[0], bias2=bias[1], bias3=bias[2], bias4=bias[3],
            peak=peakcount)

        for i in list(range(len(fidsnr))):
            data_model['snr%s' % (i+1)] = fidsnr[i]

        source = ColumnDataSource(data=dict(
            x=data_model[self.xaxis],
            y=data_model[self.yaxis]
        ))

        def style(p):
            # Title
            p.title.align = 'center'
            p.title.text_font_size = '20pt'
            p.title.text_font = 'serif'

            # Axis titles
            p.xaxis.axis_label_text_font_size = '14pt'
            p.xaxis.axis_label_text_font_style = 'bold'
            p.yaxis.axis_label_text_font_size = '14pt'
            p.yaxis.axis_label_text_font_style = 'bold'

            # Tick labels
            p.xaxis.major_label_text_font_size = '12pt'
            p.yaxis.major_label_text_font_size = '12pt'

            return p

        fiber_tooltip = """
                    <div>
                        <div>
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">x: </span>
                            <span style="font-size: 13px; color: #515151">@x</span>
                        </div>
                        <div>
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
                            <span style="font-size: 13px; color: #515151;">@y</span>
                        </div>
                    </div>
                """

        hover = HoverTool(tooltips=fiber_tooltip)

        corr = pearsonr(data_model['noise1'], data_model['noise2'])

        plot = Figure(title='r: {:3.2f}'.format(corr[0]), plot_width=600, plot_height=600,
                      toolbar_location='above',
                      x_axis_label='Noise (AMP 1)', y_axis_label='Noise (AMP 2)',
                      tools=[hover, 'pan,wheel_zoom,box_select,reset'])

        q = plot.circle('x', 'y', source=source, size=8,
                        fill_color='dodgerblue',
                        hover_fill_color='blue', line_color='black')

        qa_options = ["noise%s" % i for i in list(range(1, 5))]\
            + ["bias%s" % i for i in list(range(1, 5))]\
            + ["snr%s" % (i+1) for i in list(range(len(fidsnr)))]\
            + ['peak']

        label_dict = dict(zip(qa_options,
                              ["Noise (AMP %s)" % i for i in list(range(1, 5))]
                              + ["Bias (AMP %s)" %
                                 i for i in list(range(1, 5))]
                              + ["SNR %s" % (i+1)
                                 for i in list(range(len(fidsnr)))]
                              + ['Peak Count']
                              ))

        plot = style(plot)

        hhist, hedges = np.histogram(source.data['x'], bins='sqrt')
        hzeros = np.zeros(len(hedges)-1)
        hmax = max(hhist)*1.1

        ph = Figure(tools='pan,wheel_zoom, reset', toolbar_location='left', plot_width=plot.plot_width, plot_height=200, x_range=plot.x_range,
                    y_range=(-0.1*hmax, hmax),
                    min_border=10, min_border_left=50, y_axis_location="right")

        ph.xgrid.grid_line_color = None
        ph.yaxis.major_label_orientation = 0

        qh = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:],
                     top=hhist, color="#a7bae1", line_color="black")

        # create the vertical histogram
        vhist, vedges = np.histogram(source.data['y'], bins='sqrt')
        vzeros = np.zeros(len(vedges)-1)
        vmax = max(vhist)*1.1

        pv = Figure(tools='pan,wheel_zoom, reset', toolbar_location='above', plot_width=200, plot_height=plot.plot_height, x_range=(-0.1*vmax, vmax),
                    y_range=plot.y_range, min_border=10, y_axis_location="right")
        pv.ygrid.grid_line_color = None
        pv.xaxis.major_label_orientation = -np.pi/2
        pv.background_fill_color = "#fafafa"

        qv = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:],
                     right=vhist, color="#a7bae1", line_color="black")

        self.layout = column(
            row(column(row(plot, pv), row(ph, Spacer(width=pv.width, height=ph.height)))), sizing_mode='scale_width')

    def render(self):
        y_data = plots[self.yaxis]
        outputs_y = self.models.get_outputs_json_chunk_by_camera(
            y_data['path'], self.camera, begin_date=self.start, end_date=self.end)
        x_data = plots[self.xaxis]
        outputs = self.models.get_outputs_json_chunk_by_camera(
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

        TOOLTIPS = [
            ("Camera", "@camera"),
            (y_data['display'], "@y"),
            (x_data['display'], "@x"),
            ("Exposure", "@exposure"),
        ]

        hover = HoverTool(tooltips=TOOLTIPS)

        self.p = figure(
            sizing_mode='scale_width',
            toolbar_location='above',
            x_axis_label=x_data['display'],
            y_axis_label=y_data['display'],
            plot_width=700, plot_height=300,
            active_drag="box_zoom",
            tools=[hover, 'box_zoom,wheel_zoom,pan,reset']
        )

        info = "<h3>Camera: {}<h3>".format(self.camera)
        self.render_plot(exposures, x_values, y_values, cameras)

        info_col = Div(text=info)
        layout = column(info_col, self.layout, sizing_mode='scale_width')

        return file_html(layout, CDN, "Regression")
