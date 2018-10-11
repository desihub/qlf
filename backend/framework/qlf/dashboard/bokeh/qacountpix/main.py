from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox

from bokeh.models.widgets import PreText, Div
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.models import LinearColorMapper, ColorBar

import numpy as np

from dashboard.bokeh.helper import write_description, write_info, \
    get_merged_qa_scalar_metrics

from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import alert_table, metric_table, mtable
import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html

logger = logging.getLogger(__name__)


class Countpix:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)

        countpix = mergedqa['TASKS']['CHECK_CCDs']['METRICS']
        tests = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']
        nrg = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP_NORMAL_RANGE']
        wrg = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP_WARN_RANGE']

        # ============================================
        # THIS: Given the set up in the block above,
        #       we have the bokeh plots

        name = 'LITFRAC_AMP'
        metr = countpix

        dx = [0, 1, 0, 1]
        dy = [1, 1, 0, 0]
        dz = metr[name]
        Reds = get_palette("Reds")
        mapper = LinearColorMapper(palette=Reds, low=min(dz), high=max(dz))

        dzmax, dzmin = max(dz), min(dz)
        if np.log10(dzmax) > 4 or np.log10(dzmin) < -3:
            ztext = ['{:3.2e}'.format(i) for i in dz]
            cbarformat = "%2.1e"
        elif np.log10(dzmin) > 0:
            ztext = ['{:4.3f}'.format(i) for i in dz]
            cbarformat = "%4.2f"
        else:
            ztext = ['{:5.4f}'.format(i) for i in dz]
            cbarformat = "%5.4f"

        source = ColumnDataSource(
            data=dict(
                x=dx,
                y=dy,
                y_offset1=[i+0.15 for i in dy],
                y_offset2=[i-0.05 for i in dy],

                z=dz,
                amp=['AMP %s' % i for i in range(1, 5)],
                ztext=ztext  # ['{:3.2e}'.format(i) for i in dz]
            )
        )

        cmap_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">counts: </span>
                    <span style="font-size: 13px; color: #515151">@z</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">AMP: </span>
                    <span style="font-size: 13px; color: #515151;">@amp</span>
                </div>
            </div>
        """.replace("counts:", name+":")

        hover = HoverTool(tooltips=cmap_tooltip)

        p = Figure(title=name, tools=[hover],
                   x_range=list([-0.5, 1.5]),           # length = 18
                   y_range=list([-0.5, 1.5]),  # numeros romanos
                   plot_width=450, plot_height=400, css_classes=["plot-bokeh"]
                   )

        p.grid.grid_line_color = None
        p.outline_line_color = None
        p.axis.clear

        text_props = {
            "source": source,
            "angle": 0,
            "color": "black",
            "text_color": "black",
            "text_align": "center",
            "text_baseline": "middle"
        }

        p.rect("x", "y", .98, .98, 0, source=source,
               fill_color={'field': 'z', 'transform': mapper}, fill_alpha=0.9)  # , color="color")
        p.axis.minor_tick_line_color = None

        p.text(x="x", y="y_offset2", text="ztext",
               text_font_style="bold", text_font_size="20pt", **text_props)
        p.text(x="x", y="y_offset1", text="amp",
               text_font_size="18pt", **text_props)
        formatter = PrintfTickFormatter(format=cbarformat)  # format='%2.1e')
        color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                             major_label_text_font_size='10pt', label_standoff=2, location=(0, 0), formatter=formatter, title="", title_text_baseline="alphabetic")

        p.xaxis.axis_label = "Fraction over 5 sigma read noise (per Amp)"
        p.add_layout(color_bar, 'right')

        p.xaxis.major_label_text_font_size = '0pt'
        p.yaxis.major_label_text_font_size = '0pt'
        p.xaxis.major_tick_line_color = None
        p.xaxis.minor_tick_line_color = None

        p.yaxis.major_tick_line_color = None
        p.yaxis.minor_tick_line_color = None

        # infos
        info, nlines = write_info('countpix', tests)
        txt = PreText(text=info, height=nlines*20, width=2*p.plot_width)

        from dashboard.bokeh.qlf_plot import html_table

        tb = html_table(nrng=nrg, wrng=wrg)
        tbinfo = Div(text=tb, width=400)

        info_col = Div(text=write_description('countpix'),
                       width=450)

        # Prepare tables
        comments = 'Fraction of the pixels per amp that are above CUTPIX = 5sigmas '
        metricname = 'LITFRAC_AMP'
        keyname = 'countpix'
        curexp = mergedqa['TASKS']['CHECK_CCDs']['METRICS']['LITFRAC_AMP']
        # mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_REF']
        refexp = 'N/A'
        metric_txt = metric_table(
            metricname, comments, keyname,  curexp=curexp, refexp=refexp)
        metric_txt = mtable('countpix', mergedqa, comments)

        metric_tb = Div(text=metric_txt)

        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        p,
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "Countpix")
