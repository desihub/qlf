from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox

from bokeh.models import HoverTool, ColumnDataSource, Span
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import Select
from bokeh.models.widgets import PreText, Div
from dashboard.bokeh.helper import get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import html_table, sort_obj, mtable, alert_table

from dashboard.bokeh.helper import write_description, get_palette

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html

logger = logging.getLogger(__name__)


class Skypeak:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)
        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        skypeak = mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']
        par = mergedqa['TASKS']['CHECK_SPECTRA']['PARAMS']

        gen_info = mergedqa['GENERAL_INFO']

        # ============================================
        # values to plot:
        name = 'PEAKCOUNT'
        metr = skypeak

        # ============================================
        # THIS: Given the set up in the block above,
        #       we have the bokeh plots

        my_palette = get_palette("viridis")

        peak_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">PEAKCOUNT: </span>
                    <span style="font-size: 1vw; color: #515151">@peakcount_fib</span>
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
        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        # int(selected_spectrograph)*500, (int(selected_spectrograph)+1)*500
        c1, c2 = 0, 500
        qlf_fiberid = np.arange(0, 500)  # [c1:c2]

        obj_type = sort_obj(gen_info)
        # ---------------------------------

        peak_hover = HoverTool(tooltips=peak_tooltip)

        peakcount_fib = metr['PEAKCOUNT_FIB']

        source = ColumnDataSource(data={
            'x1': gen_info['RA'][c1:c2],
            'y1': gen_info['DEC'][c1:c2],
            'peakcount_fib': peakcount_fib,
            'QLF_FIBERID': qlf_fiberid,
            'OBJ_TYPE': obj_type,

        })

        mapper = LinearColorMapper(palette=my_palette,
                                   low=0.98*np.min(peakcount_fib),
                                   high=1.02*np.max(peakcount_fib))

        radius = 0.013
        radius_hover = 0.015

        # axes limit
        xmin, xmax = [min(gen_info['RA'][:]), max(gen_info['RA'][:])]
        ymin, ymax = [min(gen_info['DEC'][:]), max(gen_info['DEC'][:])]
        xfac, yfac = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin - xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac

        p = Figure(title='PEAKCOUNT: sum of counts in peak regions ', x_axis_label='RA', y_axis_label='DEC',
                   plot_width=500, plot_height=400, tools=[peak_hover, "box_zoom,pan,reset,crosshair, tap"], active_drag="box_zoom",)

        # Color Map
        p.circle('x1', 'y1', source=source, name="data", radius=radius,
                 fill_color={'field': 'peakcount_fib', 'transform': mapper},
                 line_color='black', line_width=0.1,
                 hover_line_color='red')

        # marking the Hover point
        p.circle('x1', 'y1', source=source, name="data", radius=radius_hover, hover_fill_color={
            'field': 'peakcount_fib', 'transform': mapper}, fill_color=None, line_color=None, line_width=3, hover_line_color='red')

        #taptool = p.select(type=TapTool)
        #taptool.callback = OpenURL(url=url)

        # bokeh.pydata.org/en/latest/docs/reference/models/annotations.html
        xcolor_bar = ColorBar(color_mapper=mapper, label_standoff=13,
                              title="counts",
                              major_label_text_font_style="bold", padding=26,
                              major_label_text_align='right',
                              major_label_text_font_size="10pt",
                              location=(0, 0))

        p.add_layout(xcolor_bar, 'right')

        try:
            info_col = Div(text=write_description('skypeak'))
        except Exception as err:
            f = open('dbg', 'w')
            f.write(str(err))
            info_col = Div(text="""""")

        # ================================
        # histogram
        hist_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Frequency: </span>
                    <span style="font-size: 1vw; color: #515151">@hist</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Peakcount: </span>
                    <span style="font-size: 1vw; color: #515151;">[@left, @right]</span>
                </div>
            </div>
        """

        hist, edges = np.histogram(peakcount_fib, bins="sqrt")

        source_hist = ColumnDataSource(data={
            'hist': hist,
            'histplusone': hist+1,
            'bottom': [0] * len(hist),
            'bottomplusone': [1]*len(hist),
            'left': edges[:-1],
            'right': edges[1:]
        })

        hover = HoverTool(tooltips=hist_tooltip)

        p_hist = Figure(title='', tools=[hover, "box_zoom,pan,wheel_zoom,reset"], active_drag="box_zoom",
                        y_axis_label='Frequency + 1',
                        x_axis_label='PEAKCOUNT', background_fill_color="white",
                        plot_width=550, plot_height=300, x_axis_type="auto",    y_axis_type="log", y_range=(1, 11**(int(np.log10(max(hist)))+1)))

        p_hist.quad(top='histplusone', bottom='bottomplusone', left='left', right='right',
                    source=source_hist,
                    fill_color="dodgerblue", line_color="black", alpha=0.8,
                    hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

        # logger.info(par['PEAKCOUNT_WARN_RANGE'])
        spans = Span(location=par['PEAKCOUNT_WARN_RANGE'][0], dimension='height', line_color='yellow',
                     line_dash='dashed', line_width=3)

        p_hist.add_layout(spans)

        nrg = par['PEAKCOUNT_NORMAL_RANGE']
        wrg = par['PEAKCOUNT_WARN_RANGE']
        tb = html_table(names=['Peakcount noise'], vals=[
                        '{:.3f}'.format(skypeak['PEAKCOUNT_NOISE'])], nrng=nrg, wrng=wrg)
        tbinfo = Div(text=tb)

       # Prepare tables
        metric_txt = mtable('skypeak', mergedqa)
        metric_tb = Div(text=metric_txt)
        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        font_size = "1vw"
        for plot in [p_hist, p]:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size


        #row1 = column(p, p_hist)
        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        column(p, sizing_mode='scale_both'),
                        column(p_hist, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "SKYPEAK")
