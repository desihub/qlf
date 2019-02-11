from bokeh.plotting import figure
from bokeh.layouts import row, column

from bokeh.models import HoverTool, ColumnDataSource, Range1d

from qlf_models import QLFModels
from dashboard.bokeh.plots.descriptors.title import Title

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html

import os
from dashboard.models import Job, Process, Fibermap

spectro_data = os.environ.get('DESI_SPECTRO_DATA')

logger = logging.getLogger(__name__)


class GlobalFiber:
    def __init__(self, process_id, arm):
        self.selected_process_id = process_id
        self.selected_arm = arm

    def data_source(self, fmap):
        """ Creating data source for plots
        """
        data_model = {
            'goodfiber': [],
            'status':   [],
            'color': [],
            'cam': [],
            'OBJ_TYPE': [],
            'ra':  [],
            'dec': [],
        }

        process_id = self.selected_process_id
        joblist = [entry.camera.camera for entry in Job.objects.filter(
            process_id=process_id)]

        ra_tile = fmap.fiber_ra
        dec_tile = fmap.fiber_dec
        otype_tile = fmap.objtype

        y = []
        color = []
        status = []
        cam_inst = []
        for spec in list(range(10)):
            cam = self.selected_arm+str(spec)
            if cam in joblist:
                mergedqa = QLFModels().get_output(
                    self.selected_process_id, cam)
                countbins = mergedqa['TASKS']['CHECK_FIBERS']['METRICS']['GOOD_FIBERS']
                y = y + countbins
                color = color + ['green' if idx ==
                                 1 else 'red' for idx in countbins]
                status = status + ['GOOD' if idx ==
                                   1 else 'BAD' for idx in countbins]
            else:
                y = y + 500*['']
                color = color + ['lightgray']*500
                status = status + ['']*500
            cam_inst = cam_inst + [cam]*500

            data_model['goodfiber'] = y
            data_model['color'] = color
            data_model['status'] = status
            data_model['cam'] = cam_inst

            data_model['OBJ_TYPE'] = otype_tile
            data_model['ra'] = ra_tile
            data_model['dec'] = dec_tile

        source = ColumnDataSource(data=data_model)

        return source

    def wedge_plot(self, wedge_arm, fmap, common_source=None):
        ra_center = fmap.exposure.telra
        dec_center = fmap.exposure.teldec

        fiber_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER STATUS: </span>
                    <span style="font-size: 13px; color: #515151">@status</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 13px; color: #515151;">@ra</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 13px; color: #515151;">@dec</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">CAM: </span>
                    <span style="font-size: 13px; color: #515151;">@cam_</span>
                </div>
        """.replace('@status', '@status').replace('@cam_', '@cam')

        hover = HoverTool(tooltips=fiber_tooltip)

        source = common_source

        radius = 0.017
        radius_hover = 0.018
        plot_space=-0.1

        xrange = Range1d(start=max(source.data['ra'])-plot_space, end=min(source.data['ra'])+plot_space)
        yrange = Range1d(start=max(source.data['dec'])-plot_space, end=min(source.data['dec'])+plot_space)

        p = figure(title='FIBERS - ARM %s' % (wedge_arm),
        x_axis_label='RA',
        y_axis_label='DEC',
        tools=[hover,"box_zoom,pan,wheel_zoom,reset,lasso_select,crosshair"],
        active_drag="box_zoom",
        x_range=xrange,
        y_range=yrange,
        sizing_mode='scale_width')
        p.title.align = 'center'

        p.circle('ra', 'dec', source=source, name="data", radius=radius,
                 fill_color={'field': 'color'},
                 line_color='black', line_width=0.4,
                 hover_line_color='red')

        p.circle('ra', 'dec', source=source, name="data", radius=radius_hover,
                 hover_fill_color={'field': 'color'}, fill_color=None,
                 line_color=None, line_width=3, hover_line_color='red')

        return p

    def load_qa(self):
        process_id = self.selected_process_id
        process = Process.objects.get(pk=process_id)
        exposure = process.exposure
        fmap = Fibermap.objects.filter(exposure=exposure)[0]

        src = self.data_source(fmap)

        p = self.wedge_plot(self.selected_arm, fmap, common_source=src)
        info_col = Title().write_description('globalfiber')

        layout = column([info_col, p], sizing_mode='scale_width')

        return file_html(layout, CDN, "Global Fiber")


if __name__ == '__main__':
    print('debbuging instance')
