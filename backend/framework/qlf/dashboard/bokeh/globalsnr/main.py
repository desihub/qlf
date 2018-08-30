import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models import HoverTool, ColumnDataSource, Range1d, Label, FixedTicker
from bokeh.models import (LinearColorMapper ,    ColorBar)

import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description, get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import plot_hist, html_table
from dashboard.bokeh.helper import get_palette

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models.widgets import Div

from dashboard.models import Process, Job
from astropy.io import fits
import os

spectro_data = os.environ.get('DESI_SPECTRO_DATA')

logger = logging.getLogger(__name__)


class GlobalSnr:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph


    def data_source_arm(self, fmap, arm ):
        """ Creating data source for plots
        """
        data_model = {
            'resids':[],
            'hover': [],
            'OBJ_TYPE': [],
            'ra':  [],
            'dec': [],
            'cam':[],
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

            objlist = sorted(set(otype_tile))
            if 'SKY' in objlist:
                objlist.remove('SKY')


        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')


        ra_snr = []
        dec_snr = []
        resids_snr=[]
        ot_snr=[]
        cam_snr = []

        for spect in list(range(10)):
            cam = arm+str(spect)

            ra_petal=[]
            dec_petal=[]
            resids_petal=[]
            ot_petal = []
            cam_petal = []
            if cam in joblist:
                mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)

                med_snr = np.array( mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']["MEDIAN_SNR"])

                # color values:
                resids_petal = (mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']['SNR_RESID'])

                ra_petal = []
                dec_petal = []
                fibers_snr = []


                obj = np.arange(len(objlist))

                    
                for t in range(len(obj)):
                    otype = list(objlist)[t]
                    oid = np.where(np.array(list(objlist))==otype)[0][0]

                    if otype == 'STD':
                        fibers = mergedqa['GENERAL_INFO']['STAR_FIBERID']
                    else:
                        fibers = mergedqa['GENERAL_INFO']['%s_FIBERID'%otype]

                    fibers_snr= fibers_snr + fibers

                    for j in range(len(fibers)):
                        ras = mergedqa['GENERAL_INFO']['RA'][fibers[j]]
                        decs = mergedqa['GENERAL_INFO']['DEC'][fibers[j]]         
                        ra_petal.append(ras)
                        dec_petal.append(decs)
                        ot_petal.append(otype)


                ra_snr=ra_snr+ra_petal
                dec_snr=dec_snr+dec_petal
                resids_snr=resids_snr+ [i if i >-999 else np.nan for i in resids_petal  ]
                ot_snr= ot_snr + ot_petal   
                cam_snr = cam_snr + [cam]*len(ra_petal)            

            else:
                try:
                    ra_snr = ra_snr+  list(ra_tile[500*spect: 500*(spect +1)])
                    dec_snr = dec_snr+ list(dec_tile[500*spect: 500*(spect +1)])
                    resids_snr = resids_snr + 500*[np.nan] 
                    ot_snr = ot_snr + list(otype_tile[500*spect: 500*(spect +1)]  )
                    cam_snr = cam_snr + [str(cam)]*500     
                except Exception as err:
                    sys.exit()

        data_model['ra'] = ra_snr #ra_tile
        data_model['dec'] = dec_snr #dec_tile
        data_model['resids'] = resids_snr
        data_model['hover'] =  ['%4.3f'%(ires) for ires in  resids_snr]
        data_model['OBJ_TYPE'] = ot_snr         
        data_model['cam'] = cam_snr

        source = ColumnDataSource(data=data_model)
        return source



    def data_source(self, fmap ):
        """ Creating data source for plots
        """
        data_model = {
            'x_b':[],
            'x_r':[],
            'x_z':[],
            'OBJ_TYPE': [],
            'ra':  [],
            'dec': [],
            'cam_b':[],
            'cam_r':[],
            'cam_z':[]
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

            objlist = sorted(set(otype_tile))
            if 'SKY' in objlist:
                objlist.remove('SKY')

        except Exception as err:
            logger.info(err)
            #sys.exit('Could not load data')


        rayes_tile = []
        decyes_tile = []

        for arm in ['b','r','z']:
            fibaux = []



            y = []
            cam_inst = []
            ra_all=[]
            dec_all=[]

            for spect in list(range(1)): 
                cam = arm+str(spect)   
                if cam in joblist:
                    try:
                        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
                        
                        # Assign available objects
                        objtype = otype_tile[500*spect: 500*(spect + 1) ]

                        med_snr = np.array( mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']["MEDIAN_SNR"])
                        resids = mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']['SNR_RESID']

                        obj = np.arange(len(objlist))

                        rayes = []
                        decyes = []

                        for t in range(len(obj)):
                            otype = list(objlist)[t]
                            oid = np.where(np.array(list(objlist))==otype)[0][0]

                            if otype == 'STD':
                                fibers = mergedqa['GENERAL_INFO']['STAR_FIBERID']
                            else:
                                fibers = mergedqa['GENERAL_INFO']['%s_FIBERID'%otype]

                            fibaux = fibaux + [ 500*spect+ i for i in fibers]
        

                            for i in range(len(fibers)):
                                ras = mergedqa['GENERAL_INFO']['RA'][fibers[i]]
                                decs = mergedqa['GENERAL_INFO']['DEC'][fibers[i]]         
                                rayes.append(ras)
                                decyes.append(decs)

                        ra_all= ra_all +  rayes
                        dec_all = dec_all + decyes

                        nanresids = [i if i >-9999.  else np.nan for i in resids]

                        y = y + nanresids

                    except Exception as err:
                        sys.exit(err)

                else:
                    y = y + 500*[np.nan]
                    ra_all =  ra_all +[ i for i in ra_tile[500*spect:500*(spect + 1)]] 
                    dec_all =  dec_all+ [ i for i in dec_tile[500*spect:500*(spect + 1)]] 
                    fibaux = fibaux + list(range(500*spect, 500*(spect+1)))


                cam_inst = cam_inst +[cam]*500

                data_model['x_' + cam[0]] = y
                data_model['cam_'+cam[0]] = cam_inst

            data_model['OBJ_TYPE'] = [ otype_tile[ii] for ii in fibaux]
            data_model['ra'] = ra_all #ra_tile
            data_model['dec'] = dec_all #dec_tile

        source = ColumnDataSource(data=data_model)

        return source




    def wedge_plot(self, wedge_arm, fmap, common_source=None, sigma_kind='x'):
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
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">RESIDUAL SNR: </span>
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
                    <span style="font-size: 13px; color: #515151;">@cam_</span>
                </div>
        """
        fiber_tooltip = fiber_tooltip.replace('@y', '@hover')
        fiber_tooltip = fiber_tooltip.replace('@cam_','@cam')


        hover = HoverTool(tooltips=fiber_tooltip)

        my_palette = get_palette("bwr") #"seismic")#"RdYlBu_r")#"viridis")
        source = common_source

        try:
            sigma = source.data['resids']#['{}_'.format(sigma_kind) +wedge_arm]
            rng_min, rng_max = np.nanmin(sigma), np.nanmax(sigma)
            rng = rng_max-rng_min

            if np.isnan(rng_min) or np.isnan(rng_max):
                fill_color = 'lightgray'
            else:
                mapper = LinearColorMapper(palette= my_palette,  nan_color='darkgrey',
                                 low= -0.2 ,
                                 high= 0.2 )

                fill_color= {'field':'resids', 'transform':mapper}
        
            radius = 0.017
            radius_hover = 0.018 

            xrange = Range1d(start=ra_center +2, end=ra_center-2) 
            yrange = Range1d(start=dec_center+1.8, end=dec_center-1.8) 

            p = Figure( title='SNR (ARM {})'.format( wedge_arm)
                    , x_axis_label='RA', y_axis_label='DEC'
                    , plot_width=600, plot_height=600
                    , tools=[hover, "pan,wheel_zoom,reset,box_zoom,crosshair"]
                    , x_range = xrange, y_range=yrange
                    )

            p.title.align='center'
            p.circle('ra', 'dec', source=source, name="data", radius=radius,
                   fill_color= fill_color, 
                   line_color='black', line_width=0.4,
                   hover_line_color='red')

            p.circle('ra', 'dec', source=source, name="data", radius=radius_hover, 
                     hover_fill_color= fill_color,
                     fill_color=None,
                     line_color=None, line_width=3, hover_line_color='orange')
            
            if 'mapper' in locals():
                cbar = Figure(height=p.plot_height, 
                width=140, 
                toolbar_location=None, 
                min_border=0, 
                outline_line_color=None,
                )

                color_bar = ColorBar(color_mapper= mapper, label_standoff=14,
                            major_label_text_font_style="bold", padding = 26,
                            major_label_text_align='right',
                            major_label_text_font_size="10pt",
                            location=(0, 0))
                cbar.title.align = 'center'
                cbar.title.text_font_size = '10pt'
                cbar.add_layout(color_bar, 'left')
                p_list = [cbar, p]
            else:
                p_list = [p]

        except Exception as err:
            p_list=None
            sys.exit(err)

        return p_list



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
            fmap = fits.open('{}/{}'.format(folder, file))


             
        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')

        src_b = self.data_source_arm(fmap,'b')

               
        try:
            src_b = self.data_source_arm(fmap,'b')
            src_r = self.data_source_arm(fmap,'r')
            src_z = self.data_source_arm(fmap,'z')                        

            pb = self.wedge_plot('b', fmap, common_source=src_b)#, common_source=source)
            pr = self.wedge_plot('r', fmap, common_source=src_r)
            pz = self.wedge_plot('z', fmap, common_source=src_z)
            layout = row(   column( row(pb)),
                            column( row(pr)),
                            column( row(pz))
                        )
        except Exception as err:
            sys.exit(err)

        return file_html(layout, CDN, "Global SNR")
