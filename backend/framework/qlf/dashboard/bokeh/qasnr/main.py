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
from dashboard.bokeh.helper import write_description, write_info, \
    get_scalar_metrics
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import html_table
from dashboard.bokeh.helper import get_exposure_ids, \
    init_xy_plot, get_url_args, get_arms_and_spectrographs
from bokeh.resources import CDN
from bokeh.embed import file_html

import numpy as np
logger = logging.getLogger(__name__)


class SNR:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)
        try:
            lm = get_scalar_metrics(self.selected_process_id, cam)
            metrics, tests = lm['metrics'], lm['tests']
        except:
            sys.exit('Could not load metrics')


        if not metrics.get('snr', None):
            sys.exit('Could not load SNR')
        else:
            snr=metrics['snr']

        try:
            exptime = tests['checkHDUs']['EXPTIME']
            name_warn=[]
        except:
            exptime=1000
            name_warn = ' (exptime fixed)'
            print('EXPTIME NOT FOUND, USING 1000')

        qlf_obj = ['ELG','LRG','QSO', 'STAR']
        keys_snr=list(snr.keys())
        objst={}
        avobj = [] #available object   
        for obj in qlf_obj:
            if obj+'_FIBERID' in keys_snr:
                objst.update({obj:True})
                avobj.append(obj)
            else:
                objst.update({obj:False})



        #sort the correct vector:
        fiberlen = []
        snrlen = []
        for i, key in enumerate(avobj):
        #2#for i, key in enumerate(['ELG_FIBERID', 'STAR_FIBERID']):
            if objst[key]:
                fiberlen.append( len(snr[key+'_FIBERID']))
                snrlen.append( len(snr['SNR_MAG_TGT'][i][0]) )



        try:
            sort_idx=[ snrlen.index(fiberlen[i]) for i in range(len(avobj))]
            #2#sort_idx=[ snrlen.index(fiberlen[i]) for i in range(2)]
        except:
            #2#sort_idx=[0,1]
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


        '''
        elg_snr  = snr['SNR_MAG_TGT'][sort_idx[0]] #[2]
        #2#star_snr = snr['SNR_MAG_TGT'][sort_idx[1]]
        lrg_snr  = snr['SNR_MAG_TGT'][sort_idx[1]] #[0]
        qso_snr  = snr['SNR_MAG_TGT'][sort_idx[2]] #[1]
        star_snr = snr['SNR_MAG_TGT'][sort_idx[3]] #[3]
        '''



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
            elg.data['fiber_id'] = snr['ELG_FIBERID']
            elg.data['ra'] = [snr['RA'][i] for i in snr['ELG_FIBERID'] ]
            elg.data['dec'] = [snr['DEC'][i] for i in snr['ELG_FIBERID'] ]

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
            lrg.data['fiber_id'] = snr['LRG_FIBERID']
            lrg.data['ra'] = [snr['RA'][i] for i in snr['LRG_FIBERID'] ]
            lrg.data['dec'] = [snr['DEC'][i] for i in snr['LRG_FIBERID'] ]

            xfit, yfit = fit_func(lrg_snr[1], snr['FITCOEFF_TGT'][sort_idx[idx]])
            idx+=1
            lrg_fit.data['x'] = xfit
            lrg_fit.data['y'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                lrg_fit.data[key] = ['']*len(yfit)


        if objst['QSO']:
            qso.data['x'] = qso_snr[1] 
            qso.data['y'] = np.array(qso_snr[0] )**2    
            qso.data['fiber_id'] = snr['QSO_FIBERID']
            qso.data['ra'] = [snr['RA'][i] for i in snr['QSO_FIBERID'] ]
            qso.data['dec'] = [snr['DEC'][i] for i in snr['QSO_FIBERID'] ]
            
            xfit, yfit = fit_func(qso_snr[1], snr['FITCOEFF_TGT'][sort_idx[idx]])
            idx+=1
            qso_fit.data['x'] = xfit
            qso_fit.data['y'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                qso_fit.data[key] = ['']*len(yfit)


        if objst['STAR']:
            star.data['x'] = star_snr[1] 
            star.data['y'] = np.array(star_snr[0] )**2
            star.data['fiber_id'] = snr['STAR_FIBERID']
            star.data['ra'] = [snr['RA'][i] for i in snr['STAR_FIBERID'] ]
            star.data['dec'] = [snr['DEC'][i] for i in snr['STAR_FIBERID'] ]

            xfit, yfit = fit_func( star_snr[1], snr['FITCOEFF_TGT'][sort_idx[idx]])
            #2#xfit, yfit = fit_func( star_snr[1], snr['FITCOEFF_TGT'][sort_idx[1]])
            star_fit.data['x'] = xfit
            star_fit.data['y'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                star_fit.data[key] = ['']*len(yfit)



        #2#'''

        #2#'''

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

        #taptool = star_plot.select(type=TapTool)
        #taptool.callback = OpenURL(url=url)


        #r1=row(children=[elg_plot, lrg_plot], sizing_mode='fixed') 
        #r2=row( children=[qso_plot, star_plot], sizing_mode='fixed')
        #plot = column([r1,r2], sizing_mode='fixed')
        plot = row(elg_plot,star_plot)#column(row(elg_plot,star_plot), sizing_mode='fixed')

        # infos
        key_name = 'snr'
        info, nlines = write_info(key_name, tests[key_name])
        txt = PreText(text=info, height=nlines*20)
        info_col = Div(text=write_description('snr'))#*star_plot.plot_width)


        #---------------
        #wedges


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

        skycont=metrics['skycont']
        median = snr['MEDIAN_SNR']
        resid = snr['SNR_RESID']
        qlf_fiberid = range(0,500)
        my_palette = get_palette('bwr')



        fibersnr=[]
        obj_type=['']*500
        for i in avobj:
            fibersnr.append(snr[i+'_FIBERID'])
            for j in snr[i+'_FIBERID']:
                obj_type[j] =  i
        for j in skycont['SKYFIBERID']:
            obj_type[j] =  'SKY'

        fibersnr=fibersnr[0]
        fibersnr.sort()


        try:
            for i in qlf_fiberid:
                if i in snr['ELG_FIBERID']:
                    obj_type.append('ELG')
                    fibersnr.append(i) 
                #2#'''
                elif i in snr['QSO_FIBERID']:
                    obj_type.append('QSO')
                    fibersnr.append(i)
                elif i in snr['LRG_FIBERID']:
                    obj_type.append('LRG')
                    fibersnr.append(i)
                #2#'''
                elif i in snr['STAR_FIBERID']:
                    obj_type.append('STAR')
                    fibersnr.append(i)
                elif i in skycont['SKYFIBERID']:
                    obj_type.append('SKY')
                else:
                    obj_type.append('UNKNOWN')
        except:
            pass#obj_type = ['']*500

        source = ColumnDataSource(data={
            'x1': [snr['RA'][i] for i in fibersnr ],
            'y1': [snr['DEC'][i] for i in fibersnr ],
            'resid_snr': snr['SNR_RESID'],
            'QLF_FIBERID': fibersnr,
            'OBJ_TYPE': [obj_type[i] for i in fibersnr],

        })


        dy = (np.max(resid) - np.min(resid))*0.02
        mapper = LinearColorMapper(palette=my_palette,
                                low=np.min(resid)- dy, high= np.max(resid)+dy)
        radius = 0.013#0.015
        radius_hover = 0.015#0.0165

        # axes limit

        xmin, xmax = [min(snr['RA'][:]), max(snr['RA'][:])]
        ymin, ymax = [min(snr['DEC'][:]), max(snr['DEC'][:])]
        xfac, yfac  = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin -xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac

        p = Figure(title='Residual SNR'+name_warn
                , x_axis_label='RA', y_axis_label='DEC'
                , plot_width=500, plot_height=400
                , tools=[snr_hover, "pan,box_zoom,reset,crosshair, tap"]
                ,x_range=(left,right), y_range=(bottom, top) )
        # Color Map
        p.circle('x1', 'y1', source=source, name="data", radius=radius,
                fill_color={'field': 'resid_snr', 'transform': mapper},
                line_color='black', line_width=0.4,
                hover_line_color='red')

        # marking the Hover point
        p.circle('x1', 'y1', source=source, name="data", radius=radius_hover, hover_fill_color={
                'field': 'resid_snr', 'transform': mapper}, fill_color=None, line_color=None, line_width=3, hover_line_color='red')

        xcolor_bar = ColorBar(color_mapper=mapper, label_standoff=13,
                            title="",
                            major_label_text_font_style="bold", padding=26,
                            major_label_text_align='right',
                            major_label_text_font_size="10pt",
                            location=(0, 0))

        p.add_layout(xcolor_bar, 'right')
        taptool = p.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        #plot= gridplot([[elg_plot, lrg_plot], [qso_plot, star_plot]])

        nrg= tests['snr']['FIDSNR_NORMAL_RANGE']
        wrg= tests['snr']['FIDSNR_WARN_RANGE']
        names = ['FIDSNR %s'%i for i in avobj] #, 'FIDSNR LRG', 'FIDSNR QSO', 'FIDSNR STAR']
        vals = [ 'NaN' if  isnr == -9999 else '{:.3f}'.format(isnr) for isnr in  snr['FIDSNR_TGT'] ]
        tb = html_table( names=names, vals=vals ,  nrng=nrg, wrng=wrg  )
        tbinfo=Div(text=tb)

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
        #layout = column(widgetbox(info_col), tbinfo, p,  elg_plot, star_plot )# row(plot))# Spacer(width=800-p.plot_width, height=p.plot_height) ,, Spacer(width=700, height=500)), sizing_mode='fixed')
        #2#layout=layout( [[info_col], [tbinfo], [p], [elg_plot , star_plot]    ])
        layout = column(widgetbox(info_col, css_classes=["header"]),
            widgetbox(tbinfo, css_classes=["table-ranges"]),
            p, Div(), elg_plot, lrg_plot , qso_plot, star_plot,
            css_classes=["display-grid"])
        return file_html(layout, CDN, "MEDIAN SNR")
