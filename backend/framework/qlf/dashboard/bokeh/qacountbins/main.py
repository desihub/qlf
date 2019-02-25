from bokeh.layouts import column, widgetbox

from bokeh.models import HoverTool, ColumnDataSource, Range1d, Label
from bokeh.models import LinearColorMapper, ColorBar

from qlf_models import QLFModels
from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.plot2d.main import Plot2d
from dashboard.bokeh.helper import sort_obj

import numpy as np
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models.widgets import Div


class Countbins:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        check_fibers = mergedqa['TASKS']['CHECK_FIBERS']
        gen_info = mergedqa['GENERAL_INFO']
        flavor=mergedqa["FLAVOR"]

        countbins = check_fibers['METRICS']
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

        p = Plot2d(
            y_range=Range1d(-.1, 1.1),
            x_label="Fiber",
            y_label="Fiber Status",
            tooltip=hist_tooltip,
            title="Status",
            width=550,
            height=350,
            yscale="auto",
            hover_mode="vline",
        ).segment(hist_source).plot

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

            radius = 0.0165  
            radius_hover = 0.02  
            # centralize wedges in plots:
            ra_center=0.5*(max(ra)+min(ra))
            dec_center=0.5*(max(dec)+min(dec))
            xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
            yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

            p2 = Plot2d(
                x_range=xrange_wedge,
                y_range=yrange_wedge,
                x_label="RA",
                y_label="DEC",
                tooltip=count_tooltip,
                title="Fiber Status",
                width=400,
                height=350,
                yscale="auto"
            ).wedge(
                hist_source,
                x='x1',
                y='y1',
                field='color',
            ).plot
        else:
            p2 = Div()

        ngood = countbins['NGOODFIB']
        fracgood = ngood/500. - 1.

        info_col = Title().write_description('countbins')

       # Prepare tables
        current_exposures = [check_fibers['METRICS']['NGOODFIB']]
        if flavor == 'science':
            program = gen_info['PROGRAM'].upper()
            reference_exposures = check_fibers['PARAMS']['NGOODFIB_' +
                                                        program + '_REF']
        else:
            reference_exposures = check_fibers['PARAMS']['NGOODFIB_REF']
        keynames = ["NGOODFIB"]
        table = Table().single_table(keynames, current_exposures, reference_exposures,
         list(map(int, nrg)), list(map(int, wrg)))
        layout = column(info_col, Div(),
                        table, Div(),
                        column(p, sizing_mode='scale_both'),
                        column(p2, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "COUNTBINS")
