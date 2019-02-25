from bokeh.layouts import row, column

from bokeh.models import HoverTool, ColumnDataSource, Span
from bokeh.models import LinearColorMapper
from bokeh.models import TapTool, OpenURL, Range1d
from bokeh.models.widgets import Div
from qlf_models import QLFModels
from dashboard.bokeh.helper import sort_obj
from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.plot2d.main import Plot2d

from dashboard.bokeh.helper import get_palette

import numpy as np
from bokeh.resources import CDN
from bokeh.embed import file_html


class Skypeak:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)
        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']

        gen_info = mergedqa['GENERAL_INFO']
        ra = gen_info['RA']
        dec = gen_info['DEC']

        nrg = check_spectra['PARAMS']['PEAKCOUNT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['PEAKCOUNT_WARN_RANGE']
        current_exposures = [check_spectra['METRICS']['PEAKCOUNT']]
        program = gen_info['PROGRAM'].upper()
        reference_exposures = check_spectra['PARAMS']['PEAKCOUNT_' +
                                                      program + '_REF']

        obj_type = sort_obj(gen_info)

        my_palette = get_palette("RdYlBu_r")

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

        qlf_fiberid = np.arange(0, 500)

        peak_hover = HoverTool(tooltips=peak_tooltip)

        peakcount_fib = check_spectra['METRICS']['PEAKCOUNT_FIB']

        source = ColumnDataSource(data={
            'x1': ra, 
            'y1': dec,
            'peakcount_fib': peakcount_fib,
            'delta_peakcount_fib': np.array(peakcount_fib)-reference_exposures,
            'QLF_FIBERID': qlf_fiberid,
            'OBJ_TYPE': obj_type,

        })
        low, high = wrg
        mapper = LinearColorMapper(palette=my_palette,
                                   low=low, #0.98*np.min(peakcount_fib),
                                   high=high, #1.02*np.max(peakcount_fib))
                                   nan_color='darkgrey') 
        radius = 0.0165  
        radius_hover = 0.02

        # centralize wedges in plots:
        ra_center=0.5*(max(ra)+min(ra))
        dec_center=0.5*(max(dec)+min(dec))
        xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
        yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

        # axes limit
        xmin, xmax = [min(gen_info['RA'][:]), max(gen_info['RA'][:])]
        ymin, ymax = [min(gen_info['DEC'][:]), max(gen_info['DEC'][:])]
        xfac, yfac = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin - xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac

        wedge_plot = Plot2d(
            x_range=xrange_wedge,
            y_range=yrange_wedge,
            x_label="RA",
            y_label="DEC",
            tooltip=peak_tooltip,
            title="PEAKCOUNT",
            width=500,
            height=380,
        ).wedge(
            source,
            x='x1',
            y='y1',
            field='delta_peakcount_fib',
            mapper=mapper,
        ).plot

        info_col = Title().write_description('skypeak')

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


        p_hist = Plot2d(
            y_range=(1, 11**(int(np.log10(max(hist)))+1)),
            x_label='PEAKCOUNT',
            y_label='Frequency + 1',
            tooltip=hist_tooltip,
            title="",
            width=550,
            height=300,
            yscale="log",
            hover_mode="vline",
        ).quad(
            source_hist,
            top='histplusone',
            bottom='bottomplusone',
            line_width=1,
        )


       # Prepare tables
        keynames = ["PEAKCOUNT" for i in range(len(current_exposures))]
        table = Table().single_table(keynames, current_exposures, reference_exposures, nrg, wrg)

        layout = column(info_col, Div(),
                        table, Div(),
                        column(wedge_plot, sizing_mode='scale_both'),
                        column(p_hist, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "SKYPEAK")
