import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.helper import write_info, get_scalar_metrics, get_scalar_metrics_aux

from dashboard.bokeh.qlf_plot import html_table
from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import Span, Label
from bokeh.models import ColumnDataSource, HoverTool, TapTool, Range1d, OpenURL
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.models.widgets import Select, Slider
from dashboard.bokeh.helper import get_url_args, write_description, \
    get_scalar_metrics
from dashboard.bokeh.qlf_plot import alert_table, metric_table

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
from astropy.io import fits
import os


spectro_data = os.environ.get('DESI_SPECTRO_DATA')


class Skyresid:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        try:
            mergedqa = get_scalar_metrics_aux(self.selected_process_id, cam)
            check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
            gen_info = mergedqa['GENERAL_INFO']
            nrg = check_spectra['PARAMS']['MED_RESID_NORMAL_RANGE']
            wrg = check_spectra['PARAMS']['MED_RESID_WARN_RANGE']


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
            #logger.info(err)
            sys.exit('Could not load data')

        #check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']


        skyresid  = check_spectra['METRICS']#metrics['skyresid']
        par = check_spectra['PARAMS']#tests['skyresid']

        residmed = ''#np.median(skyresid['MED_RESID_WAVE'])
        obj_list = ['ELG','LRG','QSO', 'STAR', 'SKY']

        # ============================================
        # THIS: Given the set up in the block above, 
        #       we have the bokeh plots

        skr_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
                    <span style="font-size: 13px; color: #515151">@wl &#8491</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
                    <span style="font-size: 13px; color: #515151;">@med_resid</span>
                </div>
            </div>
        """

        wavg_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
                    <span style="font-size: 13px; color: #515151">@wl &#8491</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
                    <span style="font-size: 13px; color: #515151;">@wavg_resid</span>
                </div>
            </div>
        """

        skr_hover = HoverTool(tooltips=skr_tooltip, mode='vline')
        wavg_hover = HoverTool(tooltips=wavg_tooltip, mode='vline')


        skyres_source = ColumnDataSource(
                        data={'wl': skyresid['WAVELENGTH'],
                            'med_resid' : np.zeros(len(skyresid['WAVELENGTH'])),#skyresid['MED_RESID_WAVE'],
                            'wavg_resid': skyresid['WAVG_RES_WAVE']
                            })

        p1 = Figure(title= 'MED_RESID_WAVE', 
                    x_axis_label='Wavelength (A)', y_axis_label='Flux (counts)',
                    plot_width = 500, plot_height = 240,
                tools=[skr_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

        p1.line('wl', 'med_resid', source=skyres_source)

        p2 = Figure(title= 'WAVG_RESID_WAVE', 
                    x_axis_label='Wavelength (A)', y_axis_label='Flux (counts)',
                    plot_width = 500, plot_height = 240,
                tools=[wavg_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

        p2.line('wl', 'wavg_resid', source=skyres_source)



        p1.x_range = p2.x_range


        #--------------
        # hist fiber
        from dashboard.bokeh.qlf_plot import plot_hist
        hist_tooltip=""" 
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">MEDIAN RESID: </span>
                    <span style="font-size: 13px; color: #515151;">@median_resid</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 13px; color: #515151;">@fiberid</span>
                </div>
            </div>
                """
        hist_hover = HoverTool(tooltips=hist_tooltip)
        hist_source = ColumnDataSource(
                        data={'median_resid': np.zeros(len(skyresid['SKYCONT_FIBER'])),#skyresid['MED_RESID_FIBER'],
                            'fiberid' : skyresid['SKYCONT_FIBER'],#[str(i) for i in skyresid['SKYFIBERID'] ],
                            'x': np.arange(len(skyresid['SKYCONT_FIBER'])),
                            'left': np.arange(len(skyresid['SKYCONT_FIBER'])) -0.4,
                            'right':np.arange(len(skyresid['SKYCONT_FIBER']))+0.4,
                            'bottom':[0]*len(skyresid['SKYCONT_FIBER']),
                            })

        fiber_hist = plot_hist(hist_hover,None, ph=300, pw=450)

        fiber_hist.vbar(top='median_resid', x='x', width=0.8,
                    source=hist_source,
                    fill_color="dodgerblue", line_color="black", line_width =0.01, alpha=0.8,
                    hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
        fiber_hist.xaxis.axis_label="Fiber number"
        fiber_hist.yaxis.axis_label="Median resid."

        strx=[str(i) for i in range(len(skyresid['SKYCONT_FIBER']))]
        strf=[str(i) for i in skyresid['SKYCONT_FIBER'] ]
        fiber_hist.xaxis.major_label_overrides = dict(zip(strx,strf))

        text2=""""""
        for i in ['NSKY_FIB']:#['NBAD_PCHI','NREJ','NSKY_FIB','RESID_PER']:      
            text2=text2+ ("""<tr>
                            <td>{:>40}:</td> <td style='text-align:left'>{:}</td>
                            </tr> """.format(i,skyresid[i]))

        txt = Div(text="""<table style="text-align:right;font-size:16px;">
                                <tr>
                                    <td>{:>40}:</td><td style='text-align:left'>{:}</td>
                                </tr>
                                {}
                                <tr>
                                    <td>{:>40}:</td><td style='text-align:left'> {:}</td>
                                </tr>
                                <tr>
                                    <td>{:>40}:</td><td style='text-align:left'> {:}</td>
                                </tr>
                        </table>"""
                .format("Median of Residuals:", residmed
                        ,text2
                        ,"Residuals Normal Range",par['MED_RESID_NORMAL_RANGE']
                        , "Residuals Warning Range",par['MED_RESID_WARN_RANGE'])
                , width=p2.plot_width)


        info, nlines = write_info('skyresid', par)

        info_col=Div(text=write_description('skyresid'), width=p2.plot_width)

        resid_vals=[]
        resid_names=[]
        for i in ['NSKY_FIB']:#['MED_RESID','NREJ','NSKY_FIB']:#,'RESID_PER']:
            resid_names.append(i)
            if i == 'RESID_PER': #95% c.l. boundaries of residuals distribution
                resid_vals.append('[{:.3f}, {:.3f}]'.format(skyresid[i][0], skyresid[i][1])) 
            elif isinstance(skyresid[i], float):
                resid_vals.append('{:.3f}'.format(skyresid[i])  )
            else:
                resid_vals.append('%i'%(skyresid[i])) 
        
        resid_names= ['Number of Sky Fibers'] 
        #['Median of Residuals (sky fibers)', 'Number of reject fibers', 'Number of good sky fibers'] 
        tb = html_table(names=resid_names, vals=resid_vals, nrng=nrg, wrng=wrg  )
        tbinfo=Div(text=tb, width=400)


        
        # Spectra of Objects
        from dashboard.bokeh.helper import load_fits


        try:
            hdul = load_fits(self.selected_process_id, cam)
            wlength = hdul['WAVELENGTH'].data
        except Exception as err:
            logger.info('{}'.format(err))   


        p_s = []
        # for obj in obj_list:
        available_obj = set(fmap[1].data['OBJTYPE'])
        # if 'SKY' in available_obj:
        #     available_obj.remove('SKY')

        for obj in available_obj:
            spec_tooltip = """
                <div>
                    <div>
                        <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
                        <span style="font-size: 13px; color: #515151">@wlength &#8491</span>
                    </div>
                    <div>
                        <span style="font-size: 12px; font-weight: bold; color: #303030;">Counts: </span>
                        <span style="font-size: 13px; color: #515151;">@spec</span>
                    </div>
                </div>
            """
            spec_hover = HoverTool(tooltips=spec_tooltip, mode='vline')

            try:
                if obj == 'STD':
                    obj_name = 'STAR'
                else:
                    obj_name = obj
                arg = np.random.choice(gen_info[obj_name+'_FIBERID'],1)
                spec = hdul['FLUX'].data[arg][0]

                spec_source = ColumnDataSource(data={
                'wlength': wlength,
                'spec': spec,
                })
                p_spec = Figure(title= obj_name+' Spectrum Sample (Fiber ID: %d)'%arg, 
                    x_axis_label='Wavelength (A)', y_axis_label=obj_name+' Flux (counts)',
                    plot_width = 500, plot_height = 240,
                    tools=[spec_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

                p_spec.line('wlength', 'spec', source = spec_source)
                p_s.append(p_spec)
            except Exception as err:
                sys.exit(err)


        width_tb, height_tb = 400, 140

        alert = alert_table(nrg, wrg)
        tb_alert = Div(text=alert, width=width_tb, height=height_tb)

        info = metric_table('Sky Residuals', 'comments', 'keyname') 
        tb_metric =Div(text=info, width=width_tb, height=height_tb)


        try:
            layout = column([widgetbox(info_col, css_classes=["header"]),
                        widgetbox(tb_metric, tb_alert, css_classes=["table-ranges"])]
                        + [p2]
                        + p_s,css_classes=['display-grid-skyresid'])
        except Exception as err:
            sys.exit(err)
            

        return file_html(layout, CDN, "SKYRESID")
