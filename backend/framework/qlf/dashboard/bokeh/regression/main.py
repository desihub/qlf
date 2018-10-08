#        bokeh serve --show regression_hist.py
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
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import Figure
from bokeh.io import output_notebook, show
from scipy.stats import pearsonr
from bokeh.resources import CDN
from bokeh.embed import file_html
import json

class Regression():
    def __init__(self, xaxis, yaxis, start, end, exposures):
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.start = start
        self.end = end
        self.exposures = exposures

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
                            + ["Bias (AMP %s)" % i for i in list(range(1, 5))]
                            + ["SNR %s" % (i+1) for i in list(range(len(fidsnr)))]
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


        layout = column(row(column(row(plot, pv), row(ph, Spacer(width=pv.width, height=ph.height)))))

        return file_html(layout, CDN, "Regression")
