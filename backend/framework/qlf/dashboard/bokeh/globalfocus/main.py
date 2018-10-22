from bokeh.plotting import Figure
from bokeh.layouts import row, column

from bokeh.models import HoverTool, ColumnDataSource, Range1d
from bokeh.models import LinearColorMapper, ColorBar

from dashboard.bokeh.helper import get_merged_qa_scalar_metrics
from dashboard.bokeh.helper import get_palette

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html

import os
from dashboard.models import Job, Process, Fibermap

spectro_data = os.environ.get('DESI_SPECTRO_DATA')

logger = logging.getLogger(__name__)


class GlobalFocus:
    def __init__(self, process_id, arm):
        self.selected_process_id = process_id
        self.selected_arm = arm

    def data_source(self, fmap):
        """ Creating data source for plots
        """
        data_model = {
            'x': [],
            'w': [],
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
        w = []
        cam_inst = []
        for spec in list(range(10)):
            cam = self.selected_arm+str(spec)
            if cam in joblist:
                mergedqa = get_merged_qa_scalar_metrics(
                    self.selected_process_id, cam)
                xwsig = mergedqa['TASKS']['CHECK_CCDs']['METRICS']['XWSIGMA_FIB']
                y = y + xwsig[0]
                w = w + xwsig[1]

            else:
                y = y + 500*[np.nan]
                w = w + 500*[np.nan]

            cam_inst = cam_inst + [cam]*500

            data_model['x'] = y
            data_model['w'] = w
            data_model['cam'] = cam_inst

        data_model['OBJ_TYPE'] = otype_tile
        data_model['ra'] = ra_tile
        data_model['dec'] = dec_tile

        source = ColumnDataSource(data=data_model)

        return source

    def wedge_plot(self, wedge_arm, fmap, common_source=None, sigma_kind='x'):
        ra_center = fmap.exposure.telra
        dec_center = fmap.exposure.teldec

        fiber_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">SIGMA: </span>
                    <span style="font-size: 13px; color: #515151">@y</span>
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
                    <span style="font-size: 13px; color: #515151;">@cam</span>
                </div>
        """
        fiber_tooltip = fiber_tooltip.replace(
            'SIGMA:', '%sSIGMA:' % sigma_kind.upper())

        hover = HoverTool(tooltips=fiber_tooltip)

        my_palette = get_palette("bwr")
        source = common_source

        process_id = self.selected_process_id
        joblist = [entry.camera.camera for entry in Job.objects.filter(
            process_id=process_id)]
        if len(joblist) > 0:
            cam = joblist[0]
            mergedqa = get_merged_qa_scalar_metrics(
                self.selected_process_id, cam)
            warn_range = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['XWSIGMA_WARN_RANGE']
            arg_kind = {'x': 0, 'w': 1}
            refvalue = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['XWSIGMA_REF'][arg_kind[sigma_kind]]
            rng_warn_min, rng_warn_max = warn_range[0] + \
                refvalue, warn_range[1] + refvalue

        sigma = source.data['{}'.format(sigma_kind)]
        rng_min, rng_max = np.nanmin(sigma), np.nanmax(sigma)
        rng = rng_max-rng_min

        if np.isnan(rng_min) or np.isnan(rng_max):
            fill_color = 'lightgray'
        else:
            mapper = LinearColorMapper(palette=my_palette,  nan_color='lightgray',
                                       low=rng_warn_min,
                                       high=rng_warn_max)

            fill_color = {'field': '%s' % (sigma_kind), 'transform': mapper}

        radius = 0.017
        radius_hover = 0.018

        xrange = Range1d(start=ra_center + 2, end=ra_center-2)
        yrange = Range1d(start=dec_center+1.8, end=dec_center-1.8)

        p = Figure(title='FOCUS %s (ARM %s)' % (sigma_kind.upper(), wedge_arm), x_axis_label='RA', y_axis_label='DEC', plot_width=600, plot_height=600, tools=[hover, "box_zoom,pan,wheel_zoom,reset,lasso_select,crosshair"], active_drag="box_zoom", x_range=xrange, y_range=yrange
                   )
        p.title.align = 'center'

        p.circle('ra', 'dec', source=source, name="data", radius=radius,
                 fill_color=fill_color,
                 line_color='black', line_width=0.4,
                 hover_line_color='red')

        p.circle('ra', 'dec', source=source, name="data", radius=radius_hover,
                 hover_fill_color=fill_color,
                 fill_color=None,
                 line_color=None, line_width=3, hover_line_color='orange')

        if 'mapper' in locals():
            cbar = Figure(height=p.plot_height,
                          width=120,
                          toolbar_location=None,
                          min_border=0,
                          outline_line_color=None,
                          )

            color_bar = ColorBar(color_mapper=mapper, label_standoff=14,
                                 major_label_text_font_style="bold", padding=26,
                                 major_label_text_align='right',
                                 major_label_text_font_size="10pt",
                                 location=(0, 0))
            cbar.title.align = 'center'
            cbar.title.text_font_size = '10pt'
            cbar.add_layout(color_bar, 'left')
            p_list = [cbar, p]
        else:
            p_list = [p]

        return p_list

    def load_qa(self):
        process_id = self.selected_process_id
        process = Process.objects.get(pk=process_id)
        exposure = process.exposure

        fmap = Fibermap.objects.filter(exposure=exposure)[0]

        src = self.data_source(fmap)

        # , common_source=source)
        p = self.wedge_plot(self.selected_arm, fmap,
                            common_source=src, sigma_kind='x')
        pw = self.wedge_plot(self.selected_arm, fmap,
                             common_source=src, sigma_kind='w')
        layout = row(column(row(p), row(pw)),)

        return file_html(layout, CDN, "Global Focus")


if __name__ == '__main__':
    print('debbuging instance')
