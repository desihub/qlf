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
        outputs = self.models.get_outputs_json_chunk_by_camera(
            axis_data['path'], self.camera, begin_date=self.start, end_date=self.end)

        dates = list()
        cameras = list()
        values = list()
        exposures = list()
        dateobs = list()
        for val in outputs:
            if val['value']:
                dates.append(val['dateobs'])
                dateobs.append(val['dateobs'].strftime('%Y-%m-%d'))
                exposures.append(val['exposure_id'])
                cameras.append(self.camera)
                values.append(val['value'])

        TOOLTIPS = [
            ("Camera", "@camera"),
            ("Value", "@y"),
            ("Exposure ID", "@exposure"),
            ("Date", "@dateobs"),
        ]

        hover = HoverTool(tooltips=TOOLTIPS)

        p = Figure(toolbar_location='above',  x_axis_type="datetime", x_axis_label='Date', y_axis_label=axis_data['display'],
                   plot_width=800, plot_height=350, tools=[hover, 'pan,wheel_zoom,zoom_in, zoom_out,reset'])

        # amp_list = [
        #     [0, 'red'],
        #     [1, 'blue'],
        #     [2, 'green']
        #     # [3, 'orange']
        # ]

        # for amp in amp_list:
        source = ColumnDataSource(data=dict(
            x=dates,
            y=values,
            exposure=exposures,
            camera=cameras,
            dateobs=dateobs
        ))
        
        p.line('x', 'y', source=source)#, legend='AMP {}'.format(amp[0]), line_color=amp[1])
        p.circle('x', 'y', source=source, size=5)#, line_color=None, fill_color=amp[1])

        layout = column(p)
        return file_html(layout, CDN, "Time Series")

if __name__ == "__main__":
    ts = TimeSeries("test", "20191001", "20191001", "b0")
    ts.render()
