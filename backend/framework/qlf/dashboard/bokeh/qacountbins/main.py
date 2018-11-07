from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox

from bokeh.models import HoverTool, ColumnDataSource, Range1d, Label,\
    FixedTicker
from bokeh.models import LinearColorMapper, ColorBar

from dashboard.bokeh.helper import write_description,\
    get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import  sort_obj,\
    mtable, alert_table

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models.widgets import Div


logger = logging.getLogger(__name__)


class Countbins:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        check_fibers = mergedqa['TASKS']['CHECK_FIBERS']
        gen_info = mergedqa['GENERAL_INFO']

        countbins = check_fibers['METRICS']
        flavor=mergedqa["FLAVOR"]
        nrg = check_fibers['PARAMS']['NGOODFIB_NORMAL_RANGE']
        wrg = check_fibers['PARAMS']['NGOODFIB_WARN_RANGE']

        if flavor == "science":     
            ra = gen_info['RA']
            dec = gen_info['DEC']
        else:
            ra = ['']*500
            dec = ['']*500


        qlf_fiberid = np.arange(0, 500)  # the fiber id is giving by petal

        obj_type = sort_obj(mergedqa['GENERAL_INFO'])

        hist_tooltip = """ 
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER STATUS: </span>
                    <span style="font-size: 1vw; color: #515151;">@status</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@fiberid</span>
                </div>
            </div>
                """
        y = np.array(countbins['GOOD_FIBERS'])
        fibers = list(countbins['GOOD_FIBERS'])
        colors = ['#319b5c' if i == 1 else '#282828' for i in fibers]
        x = np.array(range(len(fibers)))
        hist_hover = HoverTool(tooltips=hist_tooltip, mode='vline')
        hist_source = ColumnDataSource(
            data={'goodfiber': y,
                  'fiberid': x,
                  'segx0': x - 0.4,
                  'segx1': x + 0.4,
                  'segy0': y,
                  'segy1': y,
                  'status': ['GOOD' if i == 1 else 'BAD' for i in y],
                  'x1': ra,
                  'y1': dec,
                  'QLF_FIBERID': qlf_fiberid,
                  'OBJ_TYPE': obj_type,
                  'color': colors
                  })

        p = Figure(tools=[hist_hover, "box_zoom, pan,wheel_zoom, lasso_select, reset, crosshair, tap"],
                    y_range=Range1d(-.1, 1.1),
                    x_axis_label='Fiber', y_axis_label=' Fiber Status',
                    active_drag="box_zoom",
                    plot_width=550,
                    plot_height=300,
                   )
        from bokeh.models.glyphs import Segment

        seg = Segment(x0='segx0', x1='segx1', y0='segy0',
                      y1='segy1', line_width=2, line_color='#1e90ff')

        p.add_glyph(hist_source, seg)
        label = Label(x=330, y=0.7, x_units='data', y_units='data',
                      text='NGOOD_FIBER: {}'.format(countbins['NGOODFIB']), render_mode='css',
                      border_line_color='black', border_line_alpha=1.0,
                      background_fill_color='white', background_fill_alpha=1.0)

        p.yaxis.ticker = FixedTicker(ticks=[0, 1])
        p.yaxis.major_label_overrides = {'0': 'bad', '1': 'good'}
        p.add_layout(label)

        # ----------------
        # Wedge

        if flavor == "science":
     
            if ra is None or dec is None:
                return 'Missing RA and DEC'

            count_tooltip = """
                <div>
                    <div>
                        <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER STATUS: </span>
                        <span style="font-size: 1vw; color: #515151">@status</span>
                    </div>
                    <div>
                        <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                        <span style="font-size: 1vw; color: #515151;">@x1</span>
                    </div>
                    <div>
                        <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                        <span style="font-size: 1vw; color: #515151;">@y1</span>
                    </div>
                    <div>
                        <span style="font-size: 1vw; font-weight: bold; color: #303030;">Obj Type: </span>
                        <span style="font-size: 1vw; color: #515151;">@OBJ_TYPE</span>
                    </div>
                </div>
            """

            hover = HoverTool(tooltips=count_tooltip)

            radius = 0.0165  
            radius_hover = 0.02  
            
            # centralize wedges in plots:
            ra_center=0.5*(max(ra)+min(ra))
            dec_center=0.5*(max(dec)+min(dec))
            xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
            yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

            p2 = Figure(title='GOOD FIBERS',
            plot_width=450,
            plot_height=400,
            active_drag="box_zoom",
            x_axis_label='RA',
            y_axis_label='DEC',
            x_range=xrange_wedge,
            y_range=yrange_wedge,
            tools=[hover,
            "box_zoom,pan,reset,lasso_select,crosshair,tap"],
            toolbar_location="right")

            # Color Map
            p2.circle('x1','y1', source=hist_source, name="data", radius=radius,
                      fill_color={'field': 'color'},
                      line_color='black', line_width=0.3,
                      hover_line_color='red')

            # marking the Hover point
            p2.circle('x1', 'y1', source=hist_source, name="data", radius=radius_hover,
                      hover_fill_color={'field': 'color'}, fill_color=None,
                      line_color=None, line_width=3, hover_line_color='red')

        else:
            p2 = Div()

        ngood = countbins['NGOODFIB']
        fracgood = ngood/500. - 1.

        info_col = Div(text=write_description('countbins'))

        font_size = "1.2vw"

        if flavor == "science":
            plist=[p, p2]
        else:
            plist=[p]
        for plot in plist:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size

       # Prepare tables
        metric_txt = mtable('countbins', mergedqa)
        metric_tb = Div(text=metric_txt)
        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        column(p, sizing_mode='scale_both'),
                        column(p2, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "COUNTBINS")
