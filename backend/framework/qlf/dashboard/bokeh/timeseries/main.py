import numpy as np

from numpy.random import random

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models.widgets import Select, TextInput
from bokeh.models import HoverTool

from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource, Spacer
from bokeh.models.widgets import Div, Select, RangeSlider
from bokeh.plotting import Figure
from bokeh.io import output_notebook, show
from scipy.stats import pearsonr
from bokeh.resources import CDN
from bokeh.embed import file_html
import json

class TimeSeries():
    def __init__(self, xaxis, start, end):
        self.xaxis = xaxis
        self.start = start
        self.end = end

    def render(self):
        try:
            data_json = json.load(
                open('/app/spectro/mock_files/QLFmock_trend_data-b0.json'))
        except Exception as err:
            print(err)
        noise = data_json['noise']
        bias = data_json['bias']
        fidsnr = data_json['fidsnr']
        peakcount = data_json['peakcount']
        time = data_json['time']


        data_model = dict(
            noise1=noise[0], noise2=noise[1], noise3=noise[2], noise4=noise[3],
            bias1=bias[0], bias2=bias[1], bias3=bias[2], bias4=bias[3],
            peak=peakcount, time=time)

        for i in list(range(len(fidsnr))):
            data_model['snr%s' % (i+1)] = fidsnr[i]

        source = ColumnDataSource(data=dict(
            x=data_model['time'],
            y=data_model[self.xaxis]
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
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">time (time_scale): </span>
                            <span style="font-size: 13px; color: #515151">@x</span>
                        </div>
                        <div>
                            <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
                            <span style="font-size: 13px; color: #515151;">@y</span>
                        </div>
                    </div>
                """

        hover = HoverTool(tooltips=fiber_tooltip)


        plot = Figure(title='', plot_width=900, plot_height=300,
                    toolbar_location='above',
                    x_axis_label='Time (time scale)', y_axis_label='Noise (AMP 1)',
                    #x_axis_type = "datetime",
                    tools=[hover, 'pan,wheel_zoom,box_select,reset'])

        q = plot.line('x', 'y', source=source,  # size= 8,
                    line_color='dodgerblue')
        #hover_fill_color='blue', line_color='black')

        qa_options = ["noise%s" % i for i in list(range(1, 5))]\
            + ["bias%s" % i for i in list(range(1, 5))]\
            + ["snr%s" % (i+1) for i in list(range(len(fidsnr)))]\
            + ['peak']

        label_dict = dict(zip(qa_options,
                            ["Noise (AMP %s)" % i for i in list(range(1, 5))]
                            + ["Bias (AMP %s)" % i for i in list(range(1, 5))]
                            + ["SNR %s" % (i+1) for i in list(range(len(fidsnr)))]
                            + ['Peak Count']
                            ))

        select_y = Select(title="", value="noise1", options=qa_options)

        plot = style(plot)
        plot.xaxis.major_label_overrides = {
            date: "{} {}".format(str(date)[4:-6], str(date)[:-4]) for i, date in enumerate(data_model['time'])
        }


        hhist, hedges = np.histogram(source.data['x'], bins='sqrt')
        hzeros = np.zeros(len(hedges)-1)
        hmax = max(hhist)*1.1


        rng_st = int(self.start)
        rng_end = int(self.end)
        st = rng_st
        end = rng_end
        source.data['x'] = data_model['time'][st:end]
        source.data['y'] = data_model[select_y.value][st:end]

        layout = column(plot)
        return file_html(layout, CDN, "Time Series")
