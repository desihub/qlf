import sys
import os
import django

qlf_root = os.environ.get('QLF_ROOT')

sys.path.append(os.path.join(qlf_root, "framework/qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

django.setup()

import numpy as np
import pandas as pd
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models import HoverTool

from bokeh.layouts import column
from bokeh.models.widgets import Div, Select, RangeSlider
from bokeh.resources import CDN
from bokeh.embed import file_html
import json
from bokeh.models import DatetimeTickFormatter
from log import get_logger
import os
from qlf_models import QLFModels
from datetime import datetime

qlf_root = os.environ.get('QLF_ROOT')

logger = get_logger(
    "qlf.bokeh",
    os.path.join(qlf_root, "logs", "bokeh.log")
)

plots = {
    'snr': {
        'display': 'SNR',
        'path': 'TASKS->CHECK_SPECTRA->METRICS->FIDSNR_TGT'
    },
    'skybrightness': {
        'display': 'SKY BRIGHTNESS',
        'path': 'TASKS->CHECK_SPECTRA->METRICS->PEAKCOUNT'
    },
    'traceshifts': {
        'display': 'TRACE SHIFTS',
        'path': 'TASKS->CHECK_SPECTRA->METRICS->XWSHIFT'
    },
    'psf': {
        'display': 'PSF FWHM',
        'path': 'TASKS->CHECK_CCDs->METRICS->XWSIGMA'
    },
    'airmass': {
        'display': 'AIRMASS',
        'path': 'GENERAL_INFO->AIRMASS'
    },
}


class TimeSeries():
    def __init__(self, yaxis, start, end, camera):
        self.yaxis = yaxis
        self.start = datetime.strptime(start, '%Y%m%d').strftime('%Y-%m-%d')
        self.end = datetime.strptime(end, '%Y%m%d').strftime('%Y-%m-%d')
        self.camera = camera
        self.models = QLFModels()

    def render(self):
        axis_data = plots[self.yaxis]
        values = self.models.get_outputs_json_chunk_by_camera(
            axis_data['path'], self.camera, begin_date=self.start, end_date=self.end)
        dic = dict()
        print(values)
        for val in values:
            if val['value']:
                dic[val['dateobs']] = {
                    "value": val['value'], "exposure": val['exposure_id'], 'dateobs': val['dateobs'].strftime('%Y-%m-%d')}
        df = pd.DataFrame.from_dict(dic, orient="index")
        df = df.fillna(0)
        df.index = pd.to_datetime(df.index)
        df.index.name = 'Date'
        df.sort_index(inplace=True)

        df['value'] = df.value
        df['exposure'] = df.exposure
        df['dateobs'] = df.dateobs

        source = ColumnDataSource(df)

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
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">Exposure: </span>
                            <span style="font-size: 13px; color: #515151">@exposure</span>
                        </div>
                        <div>
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">Value: </span>
                            <span style="font-size: 13px; color: #515151">@value</span>
                        </div>
                        <div>
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">Date Obs: </span>
                            <span style="font-size: 13px; color: #515151">@dateobs</span>
                        </div>
                    </div>
                """

        hover = HoverTool(tooltips=fiber_tooltip)

        p = Figure(toolbar_location='above',  x_axis_type="datetime", x_axis_label='Date', y_axis_label=axis_data['display'],
                   plot_width=800, plot_height=350, tools=[hover, 'pan,wheel_zoom,zoom_in, zoom_out,reset'])

        p.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        p.line('Date', 'value', source=source)
        p.square('Date', 'value', source=source)

        layout = column(p)
        return file_html(layout, CDN, "Time Series")

if __name__ == "__main__":
    ts = TimeSeries("test", "20191001", "20191001", "b0")
    ts.render()
