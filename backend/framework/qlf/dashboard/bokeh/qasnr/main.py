import os
import sys
import logging
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL
from bokeh.plotting import Figure
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import row, column, widgetbox, gridplot, layout
from bokeh.models import (LinearColorMapper ,    ColorBar)
from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter, Spacer
from dashboard.bokeh.helper import write_description, write_info
from dashboard.bokeh.helper import  get_scalar_metrics_aux
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import html_table, sort_obj, mtable, alert_table
from dashboard.bokeh.helper import get_exposure_ids, \
    init_xy_plot, get_url_args, get_arms_and_spectrographs, get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import alert_table, metric_table
from bokeh.resources import CDN
from bokeh.embed import file_html
from astropy.io import fits
import numpy as np
logger = logging.getLogger(__name__)

spectro_data = os.environ.get('DESI_SPECTRO_DATA')


class SNR:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)


        try:
            mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)

            from dashboard.models import Job, Process


            process_id = self.selected_process_id
            process = Process.objects.get(pk=process_id)
            joblist = [entry.camera.camera for entry in Job.objects.filter(process_id=process_id)]
            exposure = process.exposure
            folder = "{}/{}/{:08d}".format(
                spectro_data, exposure.night, process.exposure_id)
            file = "fibermap-{:08d}.fits".format(process.exposure_id)

            fmap = fits.open('{}/{}'.format(folder, file))
 
            otype_tile = fmap['FIBERMAP'].data['OBJTYPE']

            objlist = sorted(set(otype_tile))
            if 'SKY' in objlist:
                objlist.remove('SKY')

        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')


        gen_info = mergedqa['GENERAL_INFO']

        ra = gen_info['RA']
        dec = gen_info['DEC']
       
        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
        snr = check_spectra['METRICS']

        nrg = check_spectra['PARAMS']['FIDSNR_TGT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['FIDSNR_TGT_WARN_RANGE']

        obj_type= sort_obj(gen_info)#[""]*500


        try:
            exptime=gen_info['EXPTIME']
            name_warn=''
        except:
            exptime=1000
            name_warn = ' (exptime fixed)'


        qlf_obj = ['ELG','LRG','QSO', 'STAR']
        keys_snr=list(snr.keys())
        keys_snr=list(gen_info.keys())
        objst={}
        avobj = [] 
        for obj in qlf_obj:
            if gen_info[obj+'_FIBERID'] != None:
                objst.update({obj:True})
                avobj.append(obj)
            else:
                objst.update({obj:False})



        #sort the correct vector:
        fiberlen = []
        snrlen = []
        for i, key in enumerate(avobj):
            if objst[key]:
                fiberlen.append( len(gen_info[key+'_FIBERID'])) #fiberlen.append( len(snr[key+'_FIBERID']))
                snrlen.append( len(snr['SNR_MAG_TGT'][i][0]) ) #snrlen.append( len(snr['SNR_MAG_TGT'][i][0]) )


        # to be deprecated
        try:
            sort_idx=[ snrlen.index(fiberlen[i]) for i in range(len(avobj))]
        except:
            logger.info('Inconsistence in FIBERID and SNR lenght')   



        idx=0
        if (objst['ELG']):
            elg_snr  = snr['SNR_MAG_TGT'][sort_idx[idx]] 
            idx+=1
        if (objst['LRG']):                
            lrg_snr  = snr['SNR_MAG_TGT'][sort_idx[idx]] 
            idx+=1
        if (objst['QSO']):                
            qso_snr  = snr['SNR_MAG_TGT'][sort_idx[idx]] 
            idx+=1
        if (objst['STAR']):  
            star_snr  = snr['SNR_MAG_TGT'][sort_idx[idx]] 




        def fit_func(xdata, coeff):
            """ astro fit 
            """
            r1=0.0 #read noise
            a, b = coeff

            x = np.linspace(min(xdata), max(xdata), 1000)
            Flux = 10**(-0.4*(x - 22.5))
            y = a*Flux*exptime/np.sqrt( a*Flux*exptime + b*exptime+r1**2) 
            return x, y



        data_model = {
            'x': [],
            'y': [],
            'fiber_id': [],
            'ra': [],
            'dec': []
        }

        elg = ColumnDataSource(data=data_model.copy())
        lrg = ColumnDataSource(data=data_model.copy())
        qso = ColumnDataSource(data=data_model.copy())
        star = ColumnDataSource(data=data_model.copy())

        data_fit = {
            'x': [],
            'y': [],
            'fiber_id': [],
            'ra': [],
            'dec': []
        }
        elg_fit = ColumnDataSource(data=data_fit.copy())
        lrg_fit = ColumnDataSource(data=data_fit.copy())
        qso_fit = ColumnDataSource(data=data_fit.copy())
        star_fit = ColumnDataSource(data=data_fit.copy())

        idx=0
        if objst['ELG']:
            elg.data['x'] = elg_snr[1] 
            elg.data['y'] = np.array( elg_snr[0])**2 
            elg.data['fiber_id'] = gen_info['ELG_FIBERID']
            elg.data['ra'] = [ra[i] for i in gen_info['ELG_FIBERID'] ]
            elg.data['dec'] = [dec[i] for i in gen_info['ELG_FIBERID'] ]

            xfit, yfit  = fit_func(elg_snr[1], 	snr['FITCOEFF_TGT'][sort_idx[idx]])
            idx+=1
            elg_fit.data['x'] = xfit
            elg_fit.data['y'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                elg_fit.data[key] = ['']*len(yfit)

        #2#'''
        if objst['LRG']:
            lrg.data['x'] = lrg_snr[1] 
            lrg.data['y'] = np.array(lrg_snr[0] )**2
            lrg.data['fiber_id'] = gen_info['LRG_FIBERID']
            lrg.data['ra'] = [ra[i] for i in gen_info['LRG_FIBERID'] ]
            lrg.data['dec'] = [dec[i] for i in gen_info['LRG_FIBERID'] ]

            xfit, yfit = fit_func(lrg_snr[1], snr['FITCOEFF_TGT'][sort_idx[idx]])
            idx+=1
            lrg_fit.data['x'] = xfit
            lrg_fit.data['y'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                lrg_fit.data[key] = ['']*len(yfit)


        if objst['QSO']:
            qso.data['x'] = qso_snr[1] 
            qso.data['y'] = np.array(qso_snr[0] )**2    
            qso.data['fiber_id'] = gen_info['QSO_FIBERID']
            qso.data['ra'] = [ra[i] for i in gen_info['QSO_FIBERID'] ]
            qso.data['dec'] = [dec[i] for i in gen_info['QSO_FIBERID'] ]
            
            xfit, yfit = fit_func(qso_snr[1], snr['FITCOEFF_TGT'][sort_idx[idx]])
            idx+=1
            qso_fit.data['x'] = xfit
            qso_fit.data['y'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                qso_fit.data[key] = ['']*len(yfit)


        if objst['STAR']:
            star.data['x'] = star_snr[1] 
            star.data['y'] = np.array(star_snr[0] )**2
            star.data['fiber_id'] = gen_info['STAR_FIBERID']
            star.data['ra'] = [ra[i] for i in gen_info['STAR_FIBERID'] ]
            star.data['dec'] = [dec[i] for i in gen_info['STAR_FIBERID'] ]

            xfit, yfit = fit_func( star_snr[1], snr['FITCOEFF_TGT'][sort_idx[idx]])
            #2#xfit, yfit = fit_func( star_snr[1], snr['FITCOEFF_TGT'][sort_idx[1]])
            star_fit.data['x'] = xfit
            star_fit.data['y'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                star_fit.data[key] = ['']*len(yfit)




        # here we make the plots
        html_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">SNR^2: </span>
                    <span style="font-size: 13px; color: #515151;">@y</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">DECAM_R: </span>
                    <span style="font-size: 13px; color: #515151;">@x</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Fiber ID: </span>
                    <span style="font-size: 13px; color: #515151;">@fiber_id</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 13px; color: #515151;">@ra</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Dec: </span>
                    <span style="font-size: 13px; color: #515151">@dec</span>
                </div>
            </div>
        """

        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        lw=1.5
        y_plot = 'y'
        plt_scale = 'log'

        hover = HoverTool(tooltips=html_tooltip)
        elg_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        elg_plot.line(x='x', y=y_plot,source=elg_fit, color="black", line_width=lw, line_alpha=0.9)
        elg_plot.circle(x='x', y=y_plot, source=elg, color="blue", size=8, line_color='black', alpha=0.7
                    ,hover_color="blue", hover_alpha=1, hover_line_color='red')

        elg_plot.xaxis.axis_label = "DECAM_{}".format(str(self.selected_arm).upper())
        elg_plot.yaxis.axis_label = "MEDIAN SNR^2"
        elg_plot.title.text = "ELG"

        taptool = elg_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)
        #2#'''
        hover = HoverTool(tooltips=html_tooltip)
        lrg_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        lrg_plot.line(x='x', y=y_plot, source=lrg_fit, color="black", line_width=lw, line_alpha=0.9)
        lrg_plot.circle(x='x', y=y_plot, source=lrg, color="red", size=8, line_color='black', alpha=0.7
                    , hover_color="red",hover_alpha=1, hover_line_color='red')

        lrg_plot.xaxis.axis_label = "DECAM_{}".format(str(self.selected_arm).upper())
        lrg_plot.yaxis.axis_label = "MEDIAN SNR^2"
        lrg_plot.title.text = "LRG"

        taptool = lrg_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        hover = HoverTool(tooltips=html_tooltip)
        qso_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        qso_plot.line(x='x', y=y_plot, source=qso_fit, color="black", line_width=lw, line_alpha=0.9)
        qso_plot.circle(x='x', y=y_plot, source=qso, color="green", size=8, line_color='black', alpha=0.7
                    ,hover_color="green", hover_alpha=1, hover_line_color='red')

        qso_plot.xaxis.axis_label = "DECAM_{}".format(str(self.selected_arm).upper())
        qso_plot.yaxis.axis_label = "MEDIAN SNR^2"
        qso_plot.title.text = "QSO"

        taptool = qso_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)
        #2#'''
        hover = HoverTool(tooltips=html_tooltip)
        star_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        star_plot.line(x='x', y=y_plot, source=star_fit, color="black", line_width=lw, line_alpha=0.9)
        star_plot.circle(x='x', y=y_plot, source=star, color="orange", size=8, line_color='black', alpha=0.7
                    ,hover_color="orange", hover_alpha=1, hover_line_color='red')

        star_plot.xaxis.axis_label = "DECAM_{}".format(str(self.selected_arm).upper())
        star_plot.yaxis.axis_label = "MEDIAN SNR^2"
        star_plot.title.text = "STAR"


        # infos
        key_name = 'snr'
        # ['FIDMAG', 'FIDSNR_TGT_REF', 'FIDSNR_WARN_RANGE', 'FIDSNR_NORMAL_RANGE']
        info, nlines = write_info(key_name, check_spectra['PARAMS'] ) #tests[key_name])
        txt = PreText(text=info, height=nlines*20)
        info_col = Div(text=write_description('snr'))#*star_plot.plot_width)


        # --- wedges --------
        snr_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Resid: </span>
                    <span style="font-size: 13px; color: #515151">@resid_snr</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
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
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER #: </span>
                    <span style="font-size: 13px; color: #515151;">@QLF_FIBERID</span>
                </div>

            </div>
        """
        snr_hover = HoverTool(tooltips=snr_tooltip)


        median = snr['MEDIAN_SNR']
        resid = snr['SNR_RESID']

        qlf_fiberid = range(0,500)
        my_palette = get_palette('bwr')

        fibersnr_tgt=[]
        obj_type= sort_obj(gen_info)
        for i in avobj:
            fibersnr_tgt.append(gen_info[i+'_FIBERID'])

        fibersnr=[]
        for i in list(range(len(fibersnr_tgt))):
            fibersnr = fibersnr + fibersnr_tgt[i]


        obj_type = sort_obj(gen_info)

        source = ColumnDataSource(data={
            'x1': [ra[i] for i in fibersnr ],
            'y1': [dec[i] for i in fibersnr ],
            'resid_snr': resid,
            'QLF_FIBERID': fibersnr,
            'OBJ_TYPE': [obj_type[i] for i in fibersnr],
            'median': median
        })

        ra_not = []
        dec_not = []
        obj_not = []
        fiber_not = []

        for i in range(500):
            if i not in fibersnr:
                ra_not.append( ra[i])
                dec_not.append( dec[i])
                fiber_not.append(i) 
                obj_not.append( obj_type[i])

        source_not = ColumnDataSource(data={
            'x1': ra_not, 
            'y1': dec_not,
            'resid_snr': ['']*len(dec_not),           
            'QLF_FIBERID': fiber_not,
            'OBJ_TYPE': obj_not
        })

        rmax, rmin = np.nanmax(resid), np.nanmin(resid)

        if np.isnan(rmax) or np.isnan(rmin):
            fill_color = 'lightgray'
        else:
            dy = (rmax - rmin)*0.1
            mapper = LinearColorMapper(palette=my_palette, nan_color='lightgray',
                        low= rmin- dy, high= rmax+dy)
            fill_color = {'field':'resid_snr', 'transform':mapper}
    

        radius = 0.013
        radius_hover = 0.015

        # axes limit
        xmin, xmax = [min(ra[:]), max(ra[:])]
        ymin, ymax = [min(dec[:]), max(dec[:])]
        xfac, yfac  = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin -xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac

        p = Figure(title='Residual SNR'+name_warn
                , x_axis_label='RA', y_axis_label='DEC'
                , plot_width=380, plot_height=380
                , tools=[snr_hover, "pan,box_zoom,reset,crosshair, tap"]
                ) #,x_range=(left,right), y_range=(bottom, top) )

        # Color Map
        p.circle('x1', 'y1', source=source, name="data", radius=radius,
                fill_color= fill_color, #{'field': 'resid_snr', 'transform': mapper},
                line_color='black', line_width=0.4,
                hover_line_color='red')

        # marking the Hover point
        p.circle('x1', 'y1', source=source, name="data", radius=radius_hover, 
            hover_fill_color= fill_color, #{'field': 'resid_snr', 'transform': mapper}, 
            fill_color=None, line_color=None, line_width=3, hover_line_color='red')

        p.circle('x1', 'y1', source= source_not, radius= radius, 
                    fill_color = 'lightgray', line_color=None, line_width=0.3)

        cbar = Figure(height=p.plot_height, 
                width=120, 
                toolbar_location=None, 
                min_border=0, 
                outline_line_color=None,
                )

        xcolor_bar = ColorBar(color_mapper=mapper, label_standoff=13,
                            title="",
                            major_label_text_font_style="bold", padding=26,
                            major_label_text_align='right',
                            major_label_text_font_size="10pt",
                            location=(0, 0))
        cbar.title.align = 'center'
        cbar.title.text_font_size = '10pt'
        cbar.add_layout(xcolor_bar, 'right')

        taptool = p.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        # Median plot

        median_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">MEDIAN: </span>
                    <span style="font-size: 13px; color: #515151">@median</span>
                </div>
       <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Resid: </span>
                    <span style="font-size: 13px; color: #515151">@resid_snr</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
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
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER #: </span>
                    <span style="font-size: 13px; color: #515151;">@QLF_FIBERID</span>
                </div>

            </div>
        """
        median_hover = HoverTool(tooltips=median_tooltip, mode='vline')

        p_m =  Figure(title= '', 
                    x_axis_label='Fiber ', y_axis_label = 'Median S/N',
                    plot_width = 500, plot_height = 240,
                    tools=[median_hover, "pan,box_zoom,reset,crosshair" ],
                    toolbar_location='above')

        p_m.vbar('QLF_FIBERID', width=1, top='median', source = source,
            hover_color='red')
        


        names = ['FIDSNR %s'%i for i in avobj] 
        vals = [ 'NaN' if  isnr == -9999 else '{:.3f}'.format(isnr) for isnr in  snr['FIDSNR_TGT'] ]
        tb = html_table( names=names, vals=vals ,  nrng=nrg, wrng=wrg  )
        tbinfo=Div(text=tb)

        width_tb, height_tb = 500, 140

        alert = alert_table(nrg, wrg)
        tb_alert = Div(text=alert, width=width_tb, height=height_tb)

        info = metric_table('Sky Residuals', 'comments', 'keyname') #, curexp=check_spectra['MED_RESID'], refexp=check_spectra['MED_RESID_REF'])
        tb_metric =Div(text=info, width=width_tb, height=height_tb)



        pltxy_h = 350
        pltxy_w = 500
        elg_plot.plot_height = pltxy_h
        elg_plot.plot_width = pltxy_w
        lrg_plot.plot_height = pltxy_h
        lrg_plot.plot_width = pltxy_w
        qso_plot.plot_height = pltxy_h
        qso_plot.plot_width = pltxy_w
        star_plot.plot_height = pltxy_h
        star_plot.plot_width = pltxy_w

        # Prepare for bokeh.layout:
        plot_snr = []
        if objst['ELG']:
            plot_snr.append(elg_plot)
        if objst['LRG']:
            plot_snr.append(lrg_plot)            
        if objst['QSO']:
            plot_snr.append(qso_plot)            
        if objst['STAR']:
            plot_snr.append(star_plot)   
        for i in list(range(4-len(plot_snr))):
            plot_snr.append(Spacer(width=pltxy_w, height=pltxy_h))

       # Prepare tables
        comments='List of average SNR for the N target type'#, N is number of target types'
        metric_txt=mtable('snr', mergedqa, comments, objtype=objlist)
        metric_tb=Div(text=metric_txt, width=500)
        alert_txt = alert_table(nrg,wrg)
        alert_tb = Div(text=alert_txt, width=500)


        layout = column(row(widgetbox(info_col)),
            row(widgetbox(metric_tb, alert_tb)),
            row( column(Spacer(width=p_m.plot_width, height=140), p_m), p,  cbar), 
            gridplot([plot_snr[0:2], plot_snr[2:4]]) 
            )
        return file_html(layout, CDN, "MEDIAN SNR")
