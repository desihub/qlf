from bokeh.plotting import Figure
from bokeh.layouts import row, column

from bokeh.models import HoverTool, ColumnDataSource, Range1d
from bokeh.models import LinearColorMapper, ColorBar

from qlf_models import QLFModels
from dashboard.bokeh.helper import get_palette

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html

import os
from dashboard.models import Job, Process, Fibermap

spectro_data = os.environ.get('DESI_SPECTRO_DATA')

logger = logging.getLogger(__name__)


class GlobalSnr:
    def __init__(self, process_id, arm):
        self.selected_process_id = process_id
        self.selected_arm = arm

    def data_source_arm(self, fmap, arm):
        """ Creating data source for plots per arm
        """
        data_model = {
            'resids': [],
            'hover': [],
            'OBJ_TYPE': [],
            'ra':  [],
            'dec': [],
            'cam': [],
            'fiber_id':[],
        }

        process_id = self.selected_process_id
        process = Process.objects.get(pk=process_id)
        joblist = [entry.camera.camera for entry in Job.objects.filter(
            process_id=process_id)]

        ra_tile = fmap.fiber_ra
        dec_tile = fmap.fiber_dec

        ra_snr  = []
        dec_snr = []
        ot_snr  = []
        cam_snr = []
        resids_snr = []
        otype_tile = ['']*5000
        fiber_id = []

        for spect in list(range(10)):
            cam = arm+str(spect)

            ra_petal = []
            dec_petal = []
            resids_petal = []
            ot_petal = []
            cam_petal = []

            if cam in joblist:
                # For each Processed petal
                mergedqa = QLFModels().get_output(
                    self.selected_process_id, cam)

                # select objlist from the given petal
                objlist = mergedqa["TASKS"]["CHECK_SPECTRA"]["METRICS"]["OBJLIST"]
                if 'SKY' in objlist:
                    objlist.remove('SKY')

                resids_petal = (
                    mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']['SNR_RESID'])
                print('size_resids', len(resids_petal))

                # complete resid_petal with NaN`s
                resids_petal = resids_petal + [np.nan]*(500-len(resids_petal))

                ra_petal = []
                dec_petal = []
                fibers_snr = []

                #Nobj = np.arange(len(objlist))
                
                # Collecting TGTs information
                for t, otype in enumerate(objlist):
                    if otype == 'STD':
                        ofibers = mergedqa['GENERAL_INFO']['STD_FIBERID']
                    else:
                        ofibers = mergedqa['GENERAL_INFO']['%s_FIBERID'%otype]

                    fibers_snr = fibers_snr + ofibers 
                
                    ot_petal= ot_petal+ [otype]*len(ofibers)

                ra_petal = [mergedqa['GENERAL_INFO']['RA'][i] for i in fibers_snr]
                dec_petal = [mergedqa['GENERAL_INFO']['DEC'][i] for i in fibers_snr]

                print("len ra_petal:", len(ra_petal))

                # Complete with sky/nonTGT information:
                sky_fiberid = mergedqa['GENERAL_INFO']['SKY_FIBERID']
                print("len sky:", len(sky_fiberid))

                ra_petal = ra_petal+[mergedqa['GENERAL_INFO']['RA'][i] for i in sky_fiberid]
                dec_petal = dec_petal+[mergedqa['GENERAL_INFO']['DEC'][i] for i in sky_fiberid]
                ot_petal= ot_petal + ['SKY']*len(sky_fiberid)
                print("len ra_petal:", len(ra_petal))
                print("len dec_petal:", len(dec_petal))
                print("len ot_petal:", len(ot_petal))
                resids_petal = [np.nan if i <= -999. or i == np.inf or i ==-np.inf 
                        else i for i in resids_petal] 
                print('len resid petal:', len(resids_petal))

                ra_snr = ra_snr+ra_petal
                dec_snr = dec_snr+dec_petal
                resids_snr = resids_snr + resids_petal
                    
                ot_snr = ot_snr + ot_petal
                fiber_id = [i+(500*spect) for i in (fibers_snr + sky_fiberid)]


            else:
                # for cams NOT processed:
                ra_snr = ra_snr + list(ra_tile[500*spect: 500*(spect + 1)])
                dec_snr = dec_snr + list(dec_tile[500*spect: 500*(spect + 1)])
                resids_snr = resids_snr + 500*[np.nan]
                ot_snr = ot_snr + list(otype_tile[500*spect: 500*(spect + 1)])
                fiber_id = fiber_id + ['']*500

            cam_snr = cam_snr + [str(cam)]*500


        data_model['ra'] = ra_snr   
        data_model['dec'] = dec_snr 
        data_model['resids'] = resids_snr
        data_model['hover'] = ['%4.3f' % (ires) for ires in resids_snr]
        data_model['OBJ_TYPE'] = ot_snr
        data_model['cam'] = cam_snr
        data_model['fiber_id'] = fiber_id

        source = ColumnDataSource(data=data_model)

        return source


    def data_source(self, fmap):
        """ Creating data source for multiple plots
        """
        data_model = {
            'x_b': [],
            'x_r': [],
            'x_z': [],
            'OBJ_TYPE': [],
            'ra':  [],
            'dec': [],
            'cam_b': [],
            'cam_r': [],
            'cam_z': []
        }

        process_id = self.selected_process_id
        joblist = [entry.camera.camera for entry in Job.objects.filter(
            process_id=process_id)]

        ra_tile = fmap.fiber_ra
        dec_tile = fmap.fiber_dec
        otype_tile = fmap.objtype

        objlist = sorted(set(otype_tile))
        if 'SKY' in objlist:
            objlist.remove('SKY')

        fibaux = []

        y = []
        cam_inst = []
        ra_all = []
        dec_all = []

        for spect in list(range(1)):
            cam = self.selected_arm+str(spect)
            if cam in joblist:
                mergedqa = QLFModels().get_output(
                    self.selected_process_id, cam)

                # Assign available objects
                objtype = otype_tile[500*spect: 500*(spect + 1)]

                med_snr = np.array(
                    mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']["MEDIAN_SNR"])
                resids = mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']['SNR_RESID']

                obj = np.arange(len(objlist))

                rayes = []
                decyes = []

                for t in range(len(obj)):
                    otype = list(objlist)[t]
                    oid = np.where(np.array(list(objlist)) == otype)[0][0]

                    if otype == 'STD':
                        fibers = mergedqa['GENERAL_INFO']['STAR_FIBERID']
                    else:
                        fibers = mergedqa['GENERAL_INFO']['%s_FIBERID' % otype]

                    fibaux = fibaux + [500*spect + i for i in fibers]

                    for i in range(len(fibers)):
                        ras = mergedqa['GENERAL_INFO']['RA'][fibers[i]]
                        decs = mergedqa['GENERAL_INFO']['DEC'][fibers[i]]
                        rayes.append(ras)
                        decyes.append(decs)

                ra_all = ra_all + rayes
                dec_all = dec_all + decyes

                nanresids = [i if i > -9999. else np.nan for i in resids]

                y = y + nanresids

            else:
                y = y + 500*[np.nan]
                ra_all = ra_all + \
                    [i for i in ra_tile[500*spect:500*(spect + 1)]]
                dec_all = dec_all + \
                    [i for i in dec_tile[500*spect:500*(spect + 1)]]
                fibaux = fibaux + list(range(500*spect, 500*(spect+1)))

            cam_inst = cam_inst + [cam]*500

            data_model['x_' + cam[0]] = y
            data_model['cam_'+cam[0]] = cam_inst

        data_model['OBJ_TYPE'] = [otype_tile[ii] for ii in fibaux]
        data_model['ra'] = ra_all
        data_model['dec'] = dec_all

        source = ColumnDataSource(data=data_model)

        return source

    def wedge_plot(self, wedge_arm, fmap, common_source=None, sigma_kind='x'):
        ra_center = fmap.exposure.telra
        dec_center = fmap.exposure.teldec

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
                    <span style="font-size: 13px; color: #515151;">@cam</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Fiber ID: </span>
                    <span style="font-size: 13px; color: #515151;">@fiber_id</span>
                </div>
        """
        fiber_tooltip = fiber_tooltip.replace('@y', '@hover')

        hover = HoverTool(tooltips=fiber_tooltip)

        my_palette = get_palette("bwr")
        source = common_source

        sigma = source.data['resids'] 

        rng_min, rng_max = np.nanmin(sigma), np.nanmax(sigma)
        rng = rng_max-rng_min

        if np.isnan(rng_min) or np.isnan(rng_max):
            fill_color = 'lightgray'
        else:
            mapper = LinearColorMapper(palette=my_palette,  nan_color='darkgrey',
                                       low=-0.2,
                                       high=0.2)

            fill_color = {'field': 'resids', 'transform': mapper}

        radius = 0.017
        radius_hover = 0.018

        xrange = Range1d(start=ra_center + 2, end=ra_center-2)
        yrange = Range1d(start=dec_center+1.8, end=dec_center-1.8)

        p = Figure(title='SNR (ARM {})'.format(wedge_arm),
                    x_axis_label='RA', y_axis_label='DEC', 
                    plot_width=600, plot_height=600, 
                    tools=[hover, "pan,wheel_zoom,reset,box_zoom,crosshair"],
                    active_drag="box_zoom",
                    x_range=xrange, y_range=yrange
                   )

        p.title.align = 'center'
        p.circle('ra', 'dec', source=source, #name="data", 
                 radius=radius,
                 fill_color=fill_color, #fill_color,
                 line_color='black', line_width=0.4,
                 hover_line_color='red')

        p.circle('ra', 'dec', source=source, name="data",
                 radius=radius_hover,
                 hover_fill_color=fill_color,
                 fill_color=None,
                 line_color=None, line_width=3, hover_line_color='orange')


        if 'mapper' in locals():
            cbar = Figure(height=p.plot_height,
                          width=140,
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

        src_arm = self.data_source_arm(fmap, self.selected_arm)

        p = self.wedge_plot(self.selected_arm, fmap, common_source=src_arm)
        layout = row(column(row(p)))

        return file_html(layout, CDN, "Global SNR")
