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


class TimeSeries():
    def __init__(self, yaxis, start, end, camera):
        self.yaxis = yaxis
        self.start = datetime.strptime(start, '%Y%m%d').strftime('%Y-%m-%d')
        self.end = datetime.strptime(end, '%Y%m%d').strftime('%Y-%m-%d')
        self.camera = camera
        self.models = QLFModels()

    def render(self):
        # dic = {'2018-08-11': {'Yes': 157, 'Not sure': 2, 'No': 1}, '2017-08-22': {'Yes': 142, 'Not sure': 12}, '2017-08-01': {'Yes': 112, 'Others': 10, 'Not sure': 4, 'No': 9}, '2017-08-17': {'Yes': 117, 'No': 12, 'Not sure': 11, 'Others': 2}, '2017-08-25': {'Yes': 61, 'Not sure': 9}, '2017-08-23': {'Yes': 268, 'Not sure': 20, 'No': 1}, '2017-07-10': {'Yes': 123, 'Not sure': 4, 'No': 1}, '2017-08-10': {'Yes': 343, 'Not sure': 20}, '2017-07-13': {'Yes': 116, 'Others': 1, 'Not sure': 14, 'No': 2}, '2017-07-14': {'Yes': 255,
        #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             'Not sure': 22, 'No': 6}, '2017-08-07': {'Yes': 73, 'Others': 3, 'Not sure': 4, 'No': 5}, '2017-08-04': {'Not sure': 11, 'Others': 8, 'Yes': 178, 'No': 10}, '2017-08-16': {'Not sure': 10, 'Yes': 219}, '2017-07-18': {'Yes': 1, 'No': 1}, '2017-08-15': {'Yes': 301, 'Others': 4, 'Not sure': 37, 'No': 31}, '2017-08-08': {'Yes': 38, 'No': 2, 'Others': 1}, '2017-08-09': {'Yes': 120, 'Not sure': 3}, '2017-08-28': {'Yes': 206, 'Others': 2, 'Not sure': 18, 'No': 24}, '2017-08-14': {'Yes': 46, 'No': 3, 'Not sure': 5, 'Others': 7}}
        values = self.models.get_outputs_json_chunk_by_camera('TASKS->CHECK_CCDs->PARAMS->CUTPIX', self.camera, begin_date=self.start, end_date=self.end)
        dic = dict()
        for val in values:
            if val['value']:
                dic[val['dateobs']] = {"value": val['value']}
        df = pd.DataFrame.from_dict(dic, orient="index")
        df = df.fillna(0)
        df.index = pd.to_datetime(df.index)
        df.index.name = 'Date'
        df.sort_index(inplace=True)

        df['value'] = df.value

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
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">time (time_scale): </span>
                            <span style="font-size: 13px; color: #515151">@Date</span>
                        </div>
                    </div>
                """

        hover = HoverTool(tooltips=fiber_tooltip)

        p = Figure(toolbar_location='above',  x_axis_type="datetime",
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