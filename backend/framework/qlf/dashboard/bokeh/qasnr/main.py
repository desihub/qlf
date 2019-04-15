from bokeh.models import ColumnDataSource, TapTool, OpenURL
from bokeh.layouts import column, layout
from bokeh.models import LinearColorMapper
from bokeh.models.widgets import Div
from bokeh.models import Range1d
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.plot2d.main import Plot2d
from qlf_models import QLFModels
from dashboard.bokeh.helper import sort_obj
from bokeh.resources import CDN
from bokeh.embed import file_html
import numpy as np
#from dashboard.models import Job, Process, Fibermap


class SNR:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)

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
        avobj = ['STAR' if x == 'STD' else x for x in objlist]

        obj_idx = {}
        for o in qlf_obj:
            try:
                obj_idx.update({o: avobj.index(o)})
            except:
                obj_idx.update({o: None})

        try:
            exptime = gen_info['EXPTIME']
            name_warn = ''
        except:
            exptime = 1000
            name_warn = ' (exptime fixed)'

        # Sorting objects for QLF:
        obj_idx = {}
        for o in qlf_obj:
            try:
                obj_idx.update({o: avobj.index(o)})
            except:
                obj_idx.update({o: None})

        def good_idx(mag, snr):
            # Filtering measurements with good SNR & good MAG
            # Treating None (inf and Nan already treated in db)
            mag_2 = np.array([-9998 if x is None else x for x in mag])
            snr_2 = np.array([-9998 if x is None else x for x in snr])
            idx = np.arange(len(snr_2))

            # Filtering values with good mag AND snr
            return list(idx[(mag_2 > -999) & (snr_2 > 0)])

        # Removing bad snr and mag
        mag_snr = {}
        fiberid_obj = {}
        for o in avobj:
            snr_ql, mag_ql = snr['SNR_MAG_TGT'][obj_idx[o]]
            idx = good_idx(mag_ql, snr_ql)
            x = [mag_ql[i] for i in idx]
            y = [snr_ql[i] for i in idx]
            mag_snr.update({o: [y, x]})
            fiberid_obj.update({o: [gen_info['%s_FIBERID'%o][i] for i in idx ]})


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
            return np.array(x), np.array(y)

#         data_model = { 
#         ...
#         star_fit = ColumnDataSource(data=data_fit.copy())
        cds = {}
        cdsfit = {}
        for on in ['ELG', 'LRG', 'QSO', 'STAR']:
            if obj_idx[on] is not None:
                cds.update({on : 
                    ColumnDataSource(dict(
                    x  = elg_snr[1],
                    y  = np.array(elg_snr[0]),
                    y2 = np.array(elg_snr[0])**2,
                    ra = [ra[i%500] for i in gen_info['ELG_FIBERID']],
                    dec = [dec[i%500] for i in gen_info['ELG_FIBERID']],
                    fiber_id = gen_info['ELG_FIBERID']
                ))})

                xfit, yfit = fit_func(elg_snr[1],
                                      snr['FITCOEFF_TGT'][obj_idx['ELG']])

                fit = dict(
                    x = xfit,
                    y = yfit,
                    y2 =yfit**2            
                )
                for key in ['fiber_id', 'ra', 'dec']:
                    fit.update({key : ['']*len(yfit)})
                cdsfit.update({on: ColumnDataSource(fit)})

                
        if obj_idx['ELG'] is not None:
            elg = ColumnDataSource(dict(
                x  = elg_snr[1],
                y  = np.array(elg_snr[0]),
                y2 = np.array(elg_snr[0])**2,
                ra = [ra[i%500] for i in gen_info['ELG_FIBERID']],
                dec = [dec[i%500] for i in gen_info['ELG_FIBERID']],
                fiber_id = gen_info['ELG_FIBERID']
            ))

            xfit, yfit = fit_func(elg_snr[1],
                                  snr['FITCOEFF_TGT'][obj_idx['ELG']])
    
            fit = dict(
                x = xfit,
                y = yfit,
                y2 =yfit**2            
            )
            for key in ['fiber_id', 'ra', 'dec']:
                fit.update({key : ['']*len(yfit)})
            elg_fit=ColumnDataSource(fit)
        

        if obj_idx['LRG'] is not None:
            lrg = ColumnDataSource(dict(
                x  = lrg_snr[1],
                y  = np.array(lrg_snr[0]),
                y2 = np.array(lrg_snr[0])**2,
                ra = [ra[i%500] for i in fiberid_obj['LRG']],
                dec = [dec[i%500] for i in fiberid_obj['LRG']],
                fiber_id = fiberid_obj['LRG']#gen_info['LRG_FIBERID']
            ))
            

            xfit, yfit = fit_func(lrg_snr[1],
                                  snr['FITCOEFF_TGT'][obj_idx['LRG']])
            fit = dict(
                x = xfit,
                y = yfit,
                y2 =yfit**2            
            )
            for key in ['fiber_id', 'ra', 'dec']:
                fit.update({key : ['']*len(yfit)})
            lrg_fit=ColumnDataSource(fit)

        if obj_idx['QSO'] is not None:
            qso = ColumnDataSource(dict(
                x  = qso_snr[1],
                y  = np.array(qso_snr[0]),
                y2 = np.array(qso_snr[0])**2,
                ra = [ra[i%500] for i in gen_info['QSO_FIBERID']],
                dec = [dec[i%500] for i in gen_info['QSO_FIBERID']],
                fiber_id = gen_info['QSO_FIBERID']
            ))

            xfit, yfit = fit_func(qso_snr[1],
                                  snr['FITCOEFF_TGT'][obj_idx['QSO']])
            fit = dict(
                x = xfit,
                y = yfit,
                y2 =yfit**2            
            )
            for key in ['fiber_id', 'ra', 'dec']:
                fit.update({key : ['']*len(yfit)})
            qso_fit = ColumnDataSource(fit)

        if obj_idx['STAR'] is not None:
            star = ColumnDataSource(dict(
                x  = star_snr[1],
                y  = np.array(star_snr[0]),
                y2 = np.array(star_snr[0])**2,
                ra = [ra[i%500] for i in gen_info['STAR_FIBERID']],
                dec = [dec[i%500] for i in gen_info['STAR_FIBERID']],
                fiber_id = gen_info['STAR_FIBERID']
            ))

            xfit, yfit = fit_func(star_snr[1],
                                  snr['FITCOEFF_TGT'][obj_idx['STAR']])
            fit = dict(
                x = xfit,
                y = yfit,
                y2 =yfit**2            
            )
            for key in ['fiber_id', 'ra', 'dec']:
                fit.update({key : ['']*len(yfit)})
            star_fit = ColumnDataSource(fit)

            
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

        elg_plot = Plot2d(
            x_label="DECAM_{}".format(str(self.selected_arm).upper()),
            y_label="MEDIAN SNR^2",
            tooltip=html_tooltip,
            title="ELG",
            width=500,
            height=380,
            yscale="log",
        ).line(
            source=elg_fit,
            y='y2',
        ).circle(
            source=elg,

            size=8,
            y='y2',
            fill_color="blue",
        ).plot

        taptool = elg_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        lrg_plot = Plot2d(
            x_label="DECAM_{}".format(str(self.selected_arm).upper()),
            y_label="MEDIAN SNR^2",
            tooltip=html_tooltip,
            title="LRG",
            width=500,
            height=380,
            yscale="log"
        ).line(
            source=lrg_fit,
            y='y2',
        ).circle(
            source=lrg,
            size=8,
            y='y2',
            fill_color="red",
        ).plot

        taptool = lrg_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        qso_plot = Plot2d(
            x_label="DECAM_{}".format(str(self.selected_arm).upper()),
            y_label="MEDIAN SNR^2",
            tooltip=html_tooltip,
            title="QSO",
            width=500,
            height=380,
            yscale="log"
        ).line(
            source=qso_fit,
            y='y2',
        ).circle(
            source=qso,
            size=8,
            y='y2',
            fill_color="green",
        ).plot

        taptool = qso_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        star_plot = Plot2d(
            x_label="DECAM_{}".format(str(self.selected_arm).upper()),
            y_label="MEDIAN SNR^2",
            tooltip=html_tooltip,
            title="STAR",
            width=500,
            height=380,
            yscale="log",
        ).line(
            source=star_fit,
             y='y2'
        ).circle(
            source=star,
            size=8,
            y='y2',
            fill_color="yellow",
        ).plot

        taptool = star_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        # infos
        info_col = Title().write_description('snr')

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

        median = snr['MEDIAN_SNR']
        resid = snr['SNR_RESID'] # Need to remove some inf & -inf 

        # Treating dataBase Nan as np.NaN
        resid = np.array([ np.nan if ( i<=-999. or i == np.inf or i== -np.inf ) else i for i in resid])

        qlf_fiberid = range(0, 500)
        my_palette = get_palette('bwr')

        fibersnr_tgt = []
        for i in avobj:
            fibersnr_tgt.append(gen_info[i+'_FIBERID'])

        fibersnr = []
        for i in list(range(len(fibersnr_tgt))):
            fibersnr = fibersnr + fibersnr_tgt[i]

        # Median of non sky fibers in the consistent order
        median_nonsky = [median[i] for  i in fibersnr]

        source = ColumnDataSource(data={
            'x1': [ra[i%500] for i in fibersnr],
            'y1': [dec[i%500] for i in fibersnr],
            'resid_snr': resid,
            'QLF_FIBERID': fibersnr,
            'OBJ_TYPE': [obj_fiber[i%500] for i in fibersnr],
            'median': median_nonsky
        })

        ra_not = []
        dec_not = []
        obj_not = []
        fiber_not = []
        fiber_mod= []
        for fiber in fibersnr:
            fiber_mod.append(fiber%500)

        for i in range(500):
            if i not in fiber_mod:
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

        # Prevents to break in only NaN case
        rmax, rmin = np.nanmax(resid), np.nanmin(resid)

        if np.isnan(rmax) or np.isnan(rmin):
            fill_color = ['lightgray']*500
        else:
            dy = (rmax - rmin)*0.1
            mapper = LinearColorMapper(palette=my_palette, nan_color='darkgray',
                                       low=-0.2, high=0.2) #low=rmin - dy, high=rmax+dy)
            fill_color = {'field': 'resid_snr', 'transform': mapper}

        radius = 0.0165
        radius_hover = 0.02
        # centralize wedges in plots:
        ra_center = 0.5*(max(ra)+min(ra))
        dec_center = 0.5*(max(dec)+min(dec))
        xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
        yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

        # axes limit
        xmin, xmax = [min(ra[:]), max(ra[:])]
        ymin, ymax = [min(dec[:]), max(dec[:])]
        xfac, yfac = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin - xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac

        # WEDGE RESIDUAL plots
        wedge_plot = Plot2d(
            x_range=xrange_wedge,
            y_range=yrange_wedge,
            x_label="RA",
            y_label="DEC",
            tooltip=snr_tooltip,
            title='Residual SNR'+name_warn,
            width=500,
            height=380,
            yscale="auto"
        ).wedge(
            source,
            x='x1',
            y='y1',
            field='resid_snr',
            mapper=mapper,
        ).wedge(
            source_not,
            x='x1',
            y='y1',
        ).plot

        taptool = wedge_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        # -------------------
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

        median_plot = Plot2d(
            x_label="Fiber",
            y_label='Median SNR',
            tooltip=median_tooltip,
            title="",
            width=600,
            height=400,
            yscale="auto",
            hover_mode="vline",
        ).vbar(
            source,
            y="median",
            x="QLF_FIBERID",
            line_width=0.4,
        )

       # Prepare tables
        current_exposures = check_spectra['METRICS']['FIDSNR_TGT']
        program = gen_info['PROGRAM'].upper()
        reference_exposures = check_spectra['PARAMS']['FIDSNR_TGT_' +
                                                      program + '_REF']
        keynames = ["FIDSNR_TGT" + " ({})".format(i) for i in objlist]
        table = Table().single_table(keynames, current_exposures, reference_exposures, nrg, wrg)

        layout = column(info_col, Div(),
                        table, Div(),
                        column(elg_plot, sizing_mode='scale_both'),
                        column(lrg_plot, sizing_mode='scale_both'),
                        column(qso_plot, sizing_mode='scale_both'),
                        column(star_plot, sizing_mode='scale_both'),
                        column(median_plot, sizing_mode='scale_both'),
                        column(wedge_plot, sizing_mode='scale_both'),
                        css_classes=["display-grid"])
        return file_html(layout, CDN, "MEDIAN SNR")
