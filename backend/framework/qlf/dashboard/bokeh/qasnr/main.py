import os
import logging
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL
from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox, layout
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.models.widgets import PreText, Div
from bokeh.models import Spacer, Range1d
from dashboard.bokeh.helper import write_description, write_info
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import sort_obj, mtable, alert_table
from dashboard.bokeh.helper import init_xy_plot, get_merged_qa_scalar_metrics
from bokeh.resources import CDN
from bokeh.embed import file_html
import numpy as np
from dashboard.models import Job, Process, Fibermap

logger = logging.getLogger(__name__)

spectro_data = os.environ.get('DESI_SPECTRO_DATA')


class SNR:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
        
        # list of available object in petal
        objlist = mergedqa["TASKS"]["CHECK_SPECTRA"]["METRICS"]["OBJLIST"]
        if 'SKY' in objlist:
            objlist.remove('SKY')


        gen_info = mergedqa['GENERAL_INFO']

        ra = gen_info['RA']
        dec = gen_info['DEC']

        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
        snr = check_spectra['METRICS']

        nrg = check_spectra['PARAMS']['FIDSNR_TGT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['FIDSNR_TGT_WARN_RANGE']

        # Object identification in fibers:
        obj_fiber = sort_obj(gen_info) 

        qlf_obj = ['ELG', 'LRG', 'QSO', 'STAR']
        avobj = ['STAR' if x=='STD' else x for x in objlist]

        obj_idx = {}
        for o in qlf_obj:
            try:
                obj_idx.update({o:avobj.index(o)})
            except:
                obj_idx.update({o:None})
        

        try:
            exptime = gen_info['EXPTIME']
            name_warn = ''
        except:
            exptime = 1000
            name_warn = ' (exptime fixed)'


        # Sort objects for QLF: 
        obj_idx = {}
        for o in qlf_obj:
            try:
                obj_idx.update({o:avobj.index(o)})
            except:
                obj_idx.update({o:None})


        def good_idx(mag,snr):
            # Filtering measurements with good SNR & good MAG 
            # Treating None (inf and Nan already treated in db)
            mag_2 = np.array([-9998 if x is None else x for x in mag ])
            snr_2 = np.array([-9998 if x is None else x for x in snr ])
            idx = np.arange(len(snr_2))
            
            # Filtering values with good mag AND snr
            return list(idx[(mag_2> -999) & (snr_2>0) ])


        # Treating bad snr and mag
        mag_snr={}
        for o in avobj:
            snr_ql, mag_ql = snr['SNR_MAG_TGT'][obj_idx[o]]
            idx = good_idx(mag_ql, snr_ql)
            x=[mag_ql[i] for i in idx]
            y=[snr_ql[i] for i in idx]
        
            mag_snr.update({o:[y,x]})

        # Preparing xy_plot data:
        if obj_idx['ELG'] is not None:
            elg_snr = mag_snr['ELG'] 
        if obj_idx['LRG'] is not None:
            lrg_snr = mag_snr['LRG'] 
        if obj_idx['QSO'] is not None:
            qso_snr = mag_snr['QSO'] 
        if obj_idx['STAR'] is not None:
            star_snr = mag_snr['STAR'] 

        #lrg_snr = mag_snr['LRG']

        def fit_func(xdata, coeff):
            """ astro fit 
            """
            r1 = 0.0  # read noise
            a, b = coeff

            x = np.linspace(min(xdata), max(xdata), 1000)
            Flux = 10**(-0.4*(x - 22.5))
            y = a*Flux*exptime/np.sqrt(a*Flux*exptime + b*exptime+r1**2)
            return x, y


        data_model = {
            'x': [],
            'y': [],
            'y2': [],            
            'fiber_id': [],
            'ra': [],
            'dec': [],
        }

        elg = ColumnDataSource(data=data_model.copy())
        lrg = ColumnDataSource(data=data_model.copy())
        qso = ColumnDataSource(data=data_model.copy())
        star = ColumnDataSource(data=data_model.copy())

        data_fit = {
            'x': [],
            'y': [],
            'y2': [],           
            'fiber_id': [],
            'ra': [],
            'dec': []
        }

        elg_fit = ColumnDataSource(data=data_fit.copy())
        lrg_fit = ColumnDataSource(data=data_fit.copy())
        qso_fit = ColumnDataSource(data=data_fit.copy())
        star_fit = ColumnDataSource(data=data_fit.copy())

        if obj_idx['ELG'] is not None:
            elg.data['x'] = elg_snr[1]
            elg.data['y'] = np.array(elg_snr[0])
            elg.data['y2'] = np.array(elg_snr[0])**2           
            elg.data['fiber_id'] = gen_info['ELG_FIBERID']
            elg.data['ra'] = [ra[i] for i in gen_info['ELG_FIBERID']]
            elg.data['dec'] = [dec[i] for i in gen_info['ELG_FIBERID']]

            xfit, yfit = fit_func(elg_snr[1], 	
                                  snr['FITCOEFF_TGT'][obj_idx['ELG']])
            elg_fit.data['x'] = xfit
            elg_fit.data['y'] = np.array(yfit)
            elg_fit.data['y2'] = np.array(yfit)**2

            for key in ['fiber_id', 'ra', 'dec']:
                elg_fit.data[key] = ['']*len(yfit)

        if obj_idx['LRG'] is not None:
            lrg.data['x'] = lrg_snr[1]
            lrg.data['y'] = np.array(lrg_snr[0])
            lrg.data['y2'] = np.array(lrg_snr[0])**2
            lrg.data['fiber_id'] = gen_info['LRG_FIBERID']
            lrg.data['ra'] = [ra[i] for i in gen_info['LRG_FIBERID']]
            lrg.data['dec'] = [dec[i] for i in gen_info['LRG_FIBERID']]

            xfit, yfit = fit_func(lrg_snr[1],
                                  snr['FITCOEFF_TGT'][obj_idx['LRG']])
            lrg_fit.data['x'] = xfit
            lrg_fit.data['y'] = np.array(yfit)
            lrg_fit.data['y2'] = np.array(yfit)**2            
            for key in ['fiber_id', 'ra', 'dec']:
                lrg_fit.data[key] = ['']*len(yfit)

        if obj_idx['QSO'] is not None:
            qso.data['x'] = qso_snr[1]
            qso.data['y'] = np.array(qso_snr[0])
            qso.data['y2'] = np.array(qso_snr[0])**2
            qso.data['fiber_id'] = gen_info['QSO_FIBERID']
            qso.data['ra'] = [ra[i] for i in gen_info['QSO_FIBERID']]
            qso.data['dec'] = [dec[i] for i in gen_info['QSO_FIBERID']]

            xfit, yfit = fit_func( qso_snr[1], 
                                   snr['FITCOEFF_TGT'][obj_idx['QSO']])
            qso_fit.data['x'] = xfit
            qso_fit.data['y'] = np.array(yfit)
            qso_fit.data['y2'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                qso_fit.data[key] = ['']*len(yfit)

        if obj_idx['STAR'] is not None:
            star.data['x'] = star_snr[1]
            star.data['y'] = np.array(star_snr[0])
            star.data['y2'] = np.array(star_snr[0])**2
            star.data['fiber_id'] = gen_info['STAR_FIBERID']
            star.data['ra'] = [ra[i] for i in gen_info['STAR_FIBERID']]
            star.data['dec'] = [dec[i] for i in gen_info['STAR_FIBERID']]

            xfit, yfit = fit_func( star_snr[1], 
                                   snr['FITCOEFF_TGT'][obj_idx['STAR']])
            star_fit.data['x'] = xfit
            star_fit.data['y'] = np.array(yfit)
            star_fit.data['y2'] = np.array(yfit)**2
            for key in ['fiber_id', 'ra', 'dec']:
                star_fit.data[key] = ['']*len(yfit)



        html_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">SNR: </span>
                    <span style="font-size: 1vw; color: #515151;">@y</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DECAM_{}: </span>
                    <span style="font-size: 1vw; color: #515151;">@x</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Fiber ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@fiber_id</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1vw; color: #515151;">@ra</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Dec: </span>
                    <span style="font-size: 1vw; color: #515151">@dec</span>
                </div>
            </div>
        """.format(str(self.selected_arm).upper())

        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        lw = 1.5
        y_plot = 'y2'
        plt_scale = 'log'

        hover = HoverTool(tooltips=html_tooltip)


        elg_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        elg_plot.line(x='x', y=y_plot, source=elg_fit,
                      color="black", line_width=lw, line_alpha=0.9)
        elg_plot.circle(x='x', y=y_plot, source=elg, 
                        color="blue", size=8, line_color='black', alpha=0.7, 
                        hover_color="blue", hover_alpha=1, hover_line_color='red',)
        elg_plot.title.text = "ELG"

        taptool = elg_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)


        lrg_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        lrg_plot.line(x='x', y=y_plot, source=lrg_fit,
                      color="black", line_width=lw, line_alpha=0.9)
        lrg_plot.circle(x='x', y=y_plot, source=lrg,
                        color="red", size=8, line_color='black', alpha=0.7,
                        hover_color="red", hover_alpha=1, hover_line_color='red',)
        lrg_plot.title.text = "LRG"

        taptool = lrg_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)


        qso_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        qso_plot.line(x='x', y=y_plot, source=qso_fit,
                      color="black", line_width=lw, line_alpha=0.9)
        qso_plot.circle(x='x', y=y_plot, source=qso, 
                        color="green", size=8, line_color='black', alpha=0.7,
                        hover_color="green", hover_alpha=1, hover_line_color='red',)
        qso_plot.title.text = "QSO"

        taptool = qso_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)


        star_plot = init_xy_plot(hover=hover, yscale=plt_scale)
        star_plot.line(x='x', y=y_plot, source=star_fit,
                       color="black", line_width=lw, line_alpha=0.9)
        star_plot.circle(x='x', y=y_plot, source=star, 
                        color="orange", size=8, line_color='black', alpha=0.7,
                        hover_color="orange", hover_alpha=1, hover_line_color='red',)
        star_plot.title.text = "STAR"

        # infos
        key_name = 'snr'
        info, nlines = write_info(key_name, check_spectra['PARAMS'])
        txt = PreText(text=info, height=nlines*20)
        info_col = Div(text=write_description('snr'))  # *star_plot.plot_width)




        # -----------------
        #       WEDGES

        snr_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Resid: </span>
                    <span style="font-size: 1vw; color: #515151">@resid_snr</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 1vw; color: #515151;">@OBJ_TYPE</span>
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
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@QLF_FIBERID</span>
                </div>

            </div>
        """
        snr_hover = HoverTool(tooltips=snr_tooltip)

        median = snr['MEDIAN_SNR']
        resid = snr['SNR_RESID']

        qlf_fiberid = range(0, 500)
        my_palette = get_palette('bwr')

        fibersnr_tgt = []
        for i in avobj:
            fibersnr_tgt.append(gen_info[i+'_FIBERID'])

        fibersnr = []
        for i in list(range(len(fibersnr_tgt))):
            fibersnr = fibersnr + fibersnr_tgt[i]


        source = ColumnDataSource(data={
            'x1': [ra[i] for i in fibersnr],
            'y1': [dec[i] for i in fibersnr],
            'resid_snr': resid,
            'QLF_FIBERID': fibersnr,
            'OBJ_TYPE': [obj_fiber[i] for i in fibersnr],
            'median': median
        })

        ra_not = []
        dec_not = []
        obj_not = []
        fiber_not = []

        for i in range(500):
            if i not in fibersnr:
                ra_not.append(ra[i])
                dec_not.append(dec[i])
                fiber_not.append(i)
                obj_not.append(obj_fiber[i])

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
            mapper = LinearColorMapper(palette=my_palette, nan_color='darkgray',
                                       low=rmin - dy, high=rmax+dy)
            fill_color = {'field': 'resid_snr', 'transform': mapper}

        radius = 0.0165  
        radius_hover = 0.02  
        # centralize wedges in plots:
        ra_center=0.5*(max(ra)+min(ra))
        dec_center=0.5*(max(dec)+min(dec))
        xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
        yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)


        # axes limit
        xmin, xmax = [min(ra[:]), max(ra[:])]
        ymin, ymax = [min(dec[:]), max(dec[:])]
        xfac, yfac = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin - xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac



        # WEDGE RESIDUAL plots
        p_res = Figure(title='Residual SNR'+name_warn,
                    active_drag="box_zoom",
                    x_axis_label='RA',
                    y_axis_label='DEC',
                    plot_width=380,
                    plot_height=380,
                    x_range=xrange_wedge,
                    y_range=yrange_wedge,
                    tools=[snr_hover, "pan,box_zoom,reset,crosshair, tap"],)

        # Color Map
        p_res.circle('x1', 'y1', source=source, name="data", radius=radius,
                 # {'field': 'resid_snr', 'transform': mapper},
                 fill_color=fill_color,
                 line_color='black', line_width=0.4,
                 hover_line_color='red')

        # marking the Hover point
        p_res.circle('x1', 'y1', source=source, name="data", radius=radius_hover,
                 # {'field': 'resid_snr', 'transform': mapper},
                 hover_fill_color=fill_color,
                 fill_color=None, line_color=None, line_width=3,
                 hover_line_color='red')

        p_res.circle('x1', 'y1', source=source_not, radius=radius,
                 fill_color='darkgray', line_color=None, line_width=0.3)

        cbar = Figure(height=p_res.plot_height,
                      active_drag="box_zoom",
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

        taptool = p_res.select(type=TapTool)
        taptool.callback = OpenURL(url=url)


        #-------------------
        #   Median plot

        median_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">MEDIAN: </span>
                    <span style="font-size: 1vw; color: #515151">@median</span>
                </div>
       <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Resid: </span>
                    <span style="font-size: 1vw; color: #515151">@resid_snr</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 1vw; color: #515151;">@OBJ_TYPE</span>
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
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@QLF_FIBERID</span>
                </div>

            </div>
        """
        median_hover = HoverTool(tooltips=median_tooltip, mode='vline')

        p_m = Figure(title='',
                     x_axis_label='Fiber',
                     y_axis_label='Median SNR',
                     plot_height=300,
                     active_drag="box_zoom",
                     tools=[median_hover, "pan,box_zoom,reset,crosshair"],
                     toolbar_location='above')

        p_m.vbar('QLF_FIBERID', width=1, top='median', source=source,
                 hover_color='red')


       # Prepare tables
        metric_txt = mtable('snr', mergedqa, objtype=objlist)
        metric_tb = Div(text=metric_txt)

        alert_txt = alert_table(nrg, wrg)
        alert_tb = Div(text=alert_txt)


        # Common xy_plot setting:
        pltxy_h = 350
        pltxy_w = 450

        for OBJ_plot in [elg_plot, lrg_plot, qso_plot, star_plot]:
            OBJ_plot.plot_height = pltxy_h
            OBJ_plot.plot_width  = pltxy_w
            OBJ_plot.yaxis.axis_label = "MEDIAN SNR^2"
            OBJ_plot.xaxis.axis_label = "DECAM_{}".format(
                                            str(self.selected_arm).upper())

        # Common setting:
        font_size = "1.4vw"
        for plot in [elg_plot, star_plot, lrg_plot, qso_plot, p_m, p_res]:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size


        layout = column(widgetbox(info_col, css_classes=["header"]), Div(),
                        widgetbox(metric_tb), widgetbox(alert_tb),
                        column(elg_plot, sizing_mode='scale_both'),
                        column(lrg_plot, sizing_mode='scale_both'),
                        column(qso_plot, sizing_mode='scale_both'),
                        column(star_plot, sizing_mode='scale_both'),
                        column(p_m, sizing_mode='scale_both'),
                        column(p_res, sizing_mode='scale_both'),
                        css_classes=["display-grid"])
        return file_html(layout, CDN, "MEDIAN SNR")
