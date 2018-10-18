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
        'path': 'TASKS->CHECK_FIBERS->METRICS->XYSHIFTS'
    },
    'psf': {
        'display': 'PSF FWHM',
        'path': 'TASKS->CHECK_CCDs->METRICS->XWSIGMA'
    },
    'airmass': {
        'display': 'AIRMASS',
        'path': 'GENERAL_INFO->AIRMASS'
    },
    'bias': {
        'display': 'BIAS',
        'path': 'TASKS->CHECK_CCDs->METRICS->BIAS_AMP'
    },
    'noise': {
        'display': 'NOISE',
        'path': 'TASKS->CHECK_CCDs->METRICS->NOISE_AMP'
    },
}


class TimeSeries():
    def __init__(self, yaxis, start, end, camera, amp=None):
        self.yaxis = yaxis
        self.start = datetime.strptime(start, '%Y%m%d').strftime('%Y-%m-%d')
        self.end = datetime.strptime(end, '%Y%m%d').strftime('%Y-%m-%d')
        self.camera = camera
        self.models = QLFModels()
        self.amp = amp

    def single_value(self, dates, values, exposures, cameras, dateobs):
        source = ColumnDataSource(data=dict(
            x=dates,
            y=values,
            exposure=exposures,
            camera=cameras,
            dateobs=dateobs
        ))
        
        self.p.line('x', 'y', source=source)
        self.p.circle('x', 'y', source=source, size=5)

    def double_value(self, dates, values, exposures, cameras, dateobs):
        pair = [[],[]]

        for value in values:
            pair[0].append(value[0])
            pair[1].append(value[1])

        colors = [
            ['spatial width averaged over fitted lines', 'blue'],
            ['median taken over all fibers per amp', 'green']
        ]
        legends=list()
        for idx, color in enumerate(colors):
            source = ColumnDataSource(data=dict(
                x=dates,
                y=pair[idx],
                exposure=exposures,
                camera=cameras,
                dateobs=dateobs
            ))
            line = self.p.line('x', 'y', source=source, line_color=color[1])
            circle = self.p.circle('x', 'y', source=source, size=5, line_color=None, fill_color=color[1])
            legends.append(('Lower {}'.format(color[0]), [line, circle]))
        legend = Legend(items=legends, location=(0, 0))

        self.p.add_layout(legend, 'below')

    def quadruple_values(self, dates, values, exposures, cameras, dateobs, objtype=None):
        amps = [[],[],[],[]]
        for value in values:
            amps[0].append(value[0])
            amps[1].append(value[1])
            amps[2].append(value[2])
            amps[3].append(value[3])

        colors = [
            'red',
            'blue',
            'green',
            'orange'
        ]
        legends=list()
        if objtype is not None:
            for idx, color in enumerate(colors):
                source = ColumnDataSource(data=dict(
                    x=dates,
                    y=amps[idx],
                    exposure=exposures,
                    camera=cameras,
                    dateobs=dateobs
                ))
                line=self.p.line('x', 'y', source=source, line_color=color)
                circle=self.p.circle('x', 'y', source=source, size=5, line_color=None, fill_color=color)
                legends.append(('OBJ {}'.format(idx), [line, circle]))
        elif self.amp == 'all':
            for idx, color in enumerate(colors):
                source = ColumnDataSource(data=dict(
                    x=dates,
                    y=amps[idx],
                    exposure=exposures,
                    camera=cameras,
                    dateobs=dateobs
                ))
                line=self.p.line('x', 'y', source=source, line_color=color)
                circle=self.p.circle('x', 'y', source=source, size=5, line_color=None, fill_color=color)
                legends.append(('AMP {}'.format(idx), [line, circle]))
        else:
            source = ColumnDataSource(data=dict(
                x=dates,
                y=amps[int(self.amp)],
                exposure=exposures,
                camera=cameras,
                dateobs=dateobs
            ))
            line=self.p.line('x', 'y', source=source, line_color=colors[int(self.amp)])
            circle=self.p.circle('x', 'y', source=source, size=5, line_color=None, fill_color=colors[int(self.amp)])
            legends.append(('AMP {}'.format(self.amp), [line, circle]))
        legend = Legend(items=legends, location=(0, 0))

        self.p.add_layout(legend, 'below')

    def render(self):
        axis_data = plots[self.yaxis]
        outputs = self.models.get_outputs_json_chunk_by_camera(
            axis_data['path'], self.camera, begin_date=self.start, end_date=self.end)

        dates = list()
        cameras = list()
        values = list()
        exposures = list()
        dateobs = list()
        mjds=list()
        for idx,val in enumerate(outputs):
            if val['value']:
                dates.append(val['dateobs'] - timedelta(minutes=20*idx))
                dateobs.append(val['dateobs'].strftime('%Y-%m-%d'))
                exposures.append(val['exposure_id'])
                cameras.append(self.camera)
                values.append(val['value'])
                date_time=(val['dateobs'] - timedelta(minutes=20*idx)).strftime('%Y-%m-%d %H:%M:%S')
                mjds.append(Time(date_time, format='iso', scale='utc').mjd)

        TOOLTIPS = [
            ("Camera", "@camera"),
            ("Value", "@y"),
            ("Exposure ID", "@exposure"),
            ("Date", "@dateobs"),
        ]

        hover = HoverTool(tooltips=TOOLTIPS)

        self.p = figure(
            sizing_mode='scale_width',
            toolbar_location='above',
            # x_axis_type="datetime",
            x_axis_label='Date (mjd)',
            y_axis_label=axis_data['display'],
            plot_width=700, plot_height=300,
            active_drag="box_zoom",
            tools=[hover, 'box_zoom,wheel_zoom,pan,reset']
        )

        info = "<h3>Camera: {}<h3>".format(self.camera)
        if self.yaxis in ['skybrightness', 'airmass']:
            self.single_value(mjds, values, exposures, cameras, dateobs)
        elif self.yaxis in ['traceshifts', 'psf']:
            self.double_value(mjds, values, exposures, cameras, dateobs)
        elif self.yaxis in ['noise', 'bias']:
            info = "<h3>Camera: {}<h3>".format(self.camera)
            self.quadruple_values(mjds, values, exposures, cameras, dateobs)
        elif self.yaxis in ['snr']:
            self.quadruple_values(mjds, values, exposures, cameras, dateobs, ['TGT', 'SKY'])

        info_col = Div(text=info)
        layout = column(info_col, self.p, sizing_mode='scale_width')
        return file_html(layout, CDN, "Time Series")

if __name__ == "__main__":
    ts = TimeSeries("test", "20191001", "20191001", "b0")
    ts.render()
