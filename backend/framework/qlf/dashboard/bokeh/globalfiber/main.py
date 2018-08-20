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

from dashboard.models import Process, Job
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


    def data_source(self, fmap ):
        """ Creating data source for plots
        """
        data_model = {
            'goodfiber_b':[],
            'goodfiber_r':[],
            'goodfiber_z':[],
            'status_b':   [],
            'status_r':   [],
            'status_z':   [],
            'color_b': [],
            'color_r': [],
            'color_z': [],
            'cam_b': [],
            'cam_r': [],
            'cam_z': [],          
            'OBJ_TYPE': [],
            'ra':  [],
            'dec': [],
            }


        try:
            process_id = self.selected_process_id
            process = Process.objects.get(pk=process_id)
            joblist = [entry.camera.camera for entry in Job.objects.filter(process_id=process_id)]
            exposure = process.exposure
 

            ra_tile = fmap['FIBERMAP'].data['RA_OBS']
            dec_tile = fmap['FIBERMAP'].data['DEC_OBS']
            otype_tile = fmap['FIBERMAP'].data['OBJTYPE']
            fid_tile = fmap['FIBERMAP'].data['FIBER']
            ra_center = fmap['FIBERMAP'].header['TELRA']
            dec_center = fmap['FIBERMAP'].header['TELDEC']

        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')



        #for cam in [ arm+str(spec) for arm in ['b','r','z'] for spec in list(range(10))]:
        for arm in ['b','r','z']:
            y = []
            color = []
            status = []
            cam_inst = []
            for spec in list(range(10)): 
                cam = arm+str(spec)   
                if cam in joblist:
                    try:
                        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
                        countbins = mergedqa['TASKS']['CHECK_FIBERS']['METRICS']['GOOD_FIBER']
                        y = y + countbins
                        color = color + [ 'green' if idx==1 else 'red' for idx in countbins]
                        status = status + ['GOOD' if idx==1 else 'BAD' for idx in countbins]

                    except Exception as err:
                        sys.exit(err)

                else:
                    y = y + 500*['']
                    color = color + ['lightgray']*500
                    status = status + ['']*500
                cam_inst = cam_inst +[cam]*500

                data_model['goodfiber_' + cam[0]] = y
                data_model['color_'+ cam[0]] =  color
                data_model['status_'+ cam[0]] =  status
                data_model['cam_'+cam[0]] = cam_inst

            data_model['OBJ_TYPE'] = otype_tile
            data_model['ra'] = ra_tile
            data_model['dec'] = dec_tile

        source = ColumnDataSource(data=data_model)

        return source



    def wedge_plot(self, wedge_arm, fmap, common_source=None):

        try:

            ra_tile = fmap['FIBERMAP'].data['RA_OBS']
            dec_tile = fmap['FIBERMAP'].data['DEC_OBS']
            fid_tile = fmap['FIBERMAP'].data['FIBER']
            ra_center = fmap['FIBERMAP'].header['TELRA']
            dec_center = fmap['FIBERMAP'].header['TELDEC']
            otype_tile = fmap['FIBERMAP'].data['OBJTYPE']

        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')


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
        """.replace('@status', '@status_'+wedge_arm).replace('@cam_','@cam_'+wedge_arm)


        hover = HoverTool(tooltips=fiber_tooltip)

        source=common_source
        
        radius = 0.017
        radius_hover = 0.018 

        xrange = Range1d(start=ra_center +2, end=ra_center-2) 
        yrange = Range1d(start=dec_center+1.8, end=dec_center-1.8) 

        p = Figure( title='FIBERS'
                , x_axis_label='RA', y_axis_label='DEC'
                , plot_width=600, plot_height=600
                , tools=[hover, "pan,wheel_zoom,reset,lasso_select,crosshair"]
                , x_range = xrange, y_range=yrange
                )

        p.circle('ra', 'dec', source=source, name="data", radius=radius,
               fill_color= {'field':'color_'+wedge_arm}, 
               line_color='black', line_width=0.4,
               hover_line_color='red')

        p.circle('ra', 'dec', source=source, name="data", radius=radius_hover, 
                 hover_fill_color={'field': 'color_'+wedge_arm}, fill_color=None,
                 line_color=None, line_width=3, hover_line_color='red')

        return p 



    def load_qa(self):

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
            fmap = fitsfile
              
        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')

        
        src = self.data_source(fmap)

        try:
            pb = self.wedge_plot('b', fmap, common_source=src)#, common_source=source)
            pr = self.wedge_plot('r', fmap, common_source=src)
            pz = self.wedge_plot('z', fmap, common_source=src)
            layout = row( column( pb, css_classes=["display-grid-countbins"]), 
                        column(pr, css_classes=["display-grid-countbins"]),
                        column(pz, css_classes=["display-grid-countbins"])) #, pz, 
        except Exception as err:
            sys.exit(err)

        return file_html(layout, CDN, "COUNTBINS")



if __name__=='__main__':
    print('debbuging instance')
