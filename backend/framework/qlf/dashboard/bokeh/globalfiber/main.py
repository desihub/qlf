import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models import HoverTool, ColumnDataSource, Range1d, Label, FixedTicker
from bokeh.models import (LinearColorMapper ,    ColorBar)


from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description, get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import plot_hist, html_table

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models.widgets import Div

from dashboard.models import Process
from astropy.io import fits
from util import get_config

cfg = get_config()
spectro_data = cfg.get("namespace", "desi_spectro_data")

logger = logging.getLogger(__name__)


class GlobalFiber:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph

    def load_qa(self):
        #cam = self.selected_arm+str(self.selected_spectrograph)

        try:
            from dashboard.models import Job, Process

            process_id = self.selected_process_id
            process = Process.objects.get(pk=process_id)
            joblist = [entry.camera.camera for entry in Job.objects.filter(process_id=process_id)]
            exposure = process.exposure
            folder = "{}/{}/{:08d}".format(
                spectro_data, exposure.night, process.exposure_id)
            file = "fibermap-{:08d}.fits".format(process.exposure_id)
            fitsfile = fits.open('{}/{}'.format(folder, file))
            ra_tile = fitsfile['FIBERMAP'].data['RA_OBS']
            dec_tile = fitsfile['FIBERMAP'].data['DEC_OBS']
            fid_tile = fitsfile['FIBERMAP'].data['FIBER']

            y = []
            ra = []
            dec = []
            obj_type = []

            for cam in joblist:
                mergedqa = get_merged_qa_scalar_metrics(
                    self.selected_process_id, cam)
                if mergedqa:
                    countbins = mergedqa['TASKS']['CHECK_FIBERS']['METRICS']['GOOD_FIBER']
                    ra_wedge = mergedqa['GENERAL_INFO']['RA']
                    dec_wedge = mergedqa['GENERAL_INFO']['DEC']
                    y = y + countbins
                    ra = ra + ra_wedge
                    dec = dec + dec_wedge
                    obj_type = obj_type + 500*['']
              
        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')


        #obj_type = sort_obj(mergedqa['GENERAL_INFO']) #tbfixed
        fiber_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER STATUS: </span>
                    <span style="font-size: 13px; color: #515151">@status</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 13px; color: #515151;">@x1</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 13px; color: #515151;">@y1</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
                </div>
            </div>
        """


        hover = HoverTool(tooltips=fiber_tooltip)



        fid_yes = []
        for i in joblist:
            j = int(i[1:])
            fid_aux = list( range(j*500, (j+1)*500 ))
            fid_yes = fid_yes + (fid_aux)

        fid_not = list( set(fid_tile).difference(set(fid_yes))  )

        qlf_fiberid = fid_yes

        source = ColumnDataSource(
                        data={'goodfiber': y,
                            'fiberid' : fid_yes,
                            'status': ['GOOD' if i==1 else 'BAD' for i in y],
                            'x1': ra,
                            'y1': dec,   
                            'QLF_FIBERID': qlf_fiberid,
                            'OBJ_TYPE': obj_type,
                            'color': ['#319b5c' if i ==1 else 'red' for i in y]
                            })

        ra_not = []
        dec_not = []
        for i in fid_not:
            ra_not.append(ra_tile[i]) 
            dec_not.append(dec_tile[i])

        source_not = ColumnDataSource(
                        data={  'ra_tile': ra_not,
                                'dec_tile': dec_not,   
                                'color': ['lightgrey']*len(fid_not)
                            })

        p = Figure( title='FIBERS'
                , x_axis_label='RA', y_axis_label='DEC'
                , plot_width=600, plot_height=600
                , tools=[hover, "pan,wheel_zoom,reset,lasso_select,crosshair"]
                )

        radius = 0.017
        radius_hover = 0.018 
        p.circle('ra_tile', 'dec_tile', source=source_not, radius=radius,
            fill_color='color', line_color='black', line_width=0.3)
        
        p.circle('x1', 'y1', source=source, name="data", radius=radius,
                fill_color= {'field':'color'}, 
                line_color='black', line_width=0.4,
                hover_line_color='red')

        # marking the Hover point
        p.circle('x1', 'y1', source=source, name="data", radius=radius_hover, 
                  hover_fill_color={'field': 'color'}, fill_color=None,
                  line_color=None, line_width=3, hover_line_color='red')

        layout = column(p, css_classes=["display-grid-countbins"])

        return file_html(layout, CDN, "COUNTBINS")



if __name__=='__main__':
    print('debbuging instance')
