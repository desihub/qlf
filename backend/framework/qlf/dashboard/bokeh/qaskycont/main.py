from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import LinearColorMapper, ColorBar, Range1d
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import PreText, Div
from dashboard.bokeh.helper import write_info, get_palette,\
    get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import mtable, alert_table

from dashboard.bokeh.helper import write_description

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html

logger = logging.getLogger(__name__)


class Skycont:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        gen_info = mergedqa['GENERAL_INFO']
        ra = gen_info['RA']
        dec = gen_info['DEC']
        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
        skycont = check_spectra['METRICS']
        sky = skycont['SKYCONT_FIBER']
        skyfibers = gen_info['SKY_FIBERID']
        nrg = check_spectra['PARAMS']['SKYCONT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['SKYCONT_WARN_RANGE']

        ra_sky = [ra[i] for i in skyfibers]
        dec_sky = [dec[i] for i in skyfibers]

        my_palette = get_palette("viridis")

        skc_tooltips = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">SKY CONT: </span>
                    <span style="font-size: 1vw; color: #515151;">@skycont</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1vw; color: #515151;">@ra</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 1vw; color: #515151;">@dec</span>
                </div>
            </div>
        """
        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        qlf_fiberid = np.arange(0, 500)

        hover = HoverTool(tooltips=skc_tooltips)

        # sky continuum per sky fiber averaged over two continuum regions,
        #  'n' is number of sky fibers

        ra_not, dec_not = [], []
        for i in range(500):
            if i not in skyfibers:
                ra_not.append(ra[i])
                dec_not.append(dec[i])

        source2 = ColumnDataSource(data={
            'skycont': sky,
            'fiberid': skyfibers,
            'ra': ra_sky,
            'dec': dec_sky
        })

        source2_not = ColumnDataSource(data={
            'ra': ra_not,
            'dec': dec_not,
            'skycont': ['']*len(dec_not)
        })

        mapper = LinearColorMapper(palette=my_palette,
                                   low=np.min(sky),
                                   high=np.max(sky),
                                   nan_color='darkgray')

        radius = 0.0165  # 0.013
        radius_hover = 0.02  # 0.015

        # centralize wedges in plots:
        ra_center=0.5*(max(ra)+min(ra))
        dec_center=0.5*(max(dec)+min(dec))
        xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
        yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

        p2 = Figure(title='SKY_CONT',
                    x_axis_label='RA', 
                    y_axis_label='DEC',
                    plot_width=500, 
                    plot_height=380,
                    x_range=xrange_wedge, 
                    y_range=yrange_wedge,
                    tools=[hover, "pan,box_zoom, wheel_zoom,reset,tap"], 
                    active_drag="box_zoom",)

        p2.circle('ra', 'dec', source=source2, radius=radius,
                  fill_color={'field': 'skycont', 'transform': mapper},
                  line_color='black', line_width=0.3)

        # marking the Hover point
        p2.circle('ra', 'dec', source=source2, radius=radius_hover, fill_color=None, line_color=None, hover_fill_color={
                  'field': 'skycont', 'transform': mapper}, line_width=3, hover_line_color='red')

        p2.circle('ra', 'dec', source=source2_not, radius=radius,
                  fill_color='lightgray', line_color='black', line_width=0.3)

        # marking the Hover point
        p2.circle('ra', 'dec', source=source2_not, radius=radius_hover, fill_color=None,
                  line_color=None, line_width=3, hover_line_color='red', hover_fill_color='lightgrey')

        taptool = p2.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        color_bar = ColorBar(color_mapper=mapper, label_standoff=16,
                             title='counts',
                             major_label_text_font_style='bold', padding=26,
                             major_label_text_align='right',
                             major_label_text_font_size="10pt",
                             location=(0, 0))

        p2.add_layout(color_bar, 'right')

        # infos
        info, nlines = write_info('skycont', check_spectra['PARAMS'])
        txt = PreText(text=info, height=nlines*20)
        info_col = Div(text=write_description('skycont'))


       # Prepare tables
        metric_txt = mtable('skycont', mergedqa)
        metric_tb = Div(text=metric_txt)
        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)

        font_size = "1vw"
        for plot in [p2]:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size

        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        column(p2, sizing_mode='scale_both',
                               css_classes=["main-one"]),
                        css_classes=["display-grid"])

        # End of Bokeh Block
        return file_html(layout, CDN, "SKYCONT")
