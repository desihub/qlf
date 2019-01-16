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
from dashboard.models import Job, Process, Fibermap


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

        # Sort objects for QLF:
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

        # Treating bad snr and mag
        mag_snr = {}
        for o in avobj:
            snr_ql, mag_ql = snr['SNR_MAG_TGT'][obj_idx[o]]
            idx = good_idx(mag_ql, snr_ql)
            x = [mag_ql[i] for i in idx]
            y = [snr_ql[i] for i in idx]

            mag_snr.update({o: [y, x]})

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

            xfit, yfit = fit_func(qso_snr[1],
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

            xfit, yfit = fit_func(star_snr[1],
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

        mediam_plot = Plot2d(
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
        metric = Table().reference_table(keynames, current_exposures, reference_exposures)
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        column(elg_plot, sizing_mode='scale_both'),
                        column(lrg_plot, sizing_mode='scale_both'),
                        column(qso_plot, sizing_mode='scale_both'),
                        column(star_plot, sizing_mode='scale_both'),
                        column(mediam_plot, sizing_mode='scale_both'),
                        column(wedge_plot, sizing_mode='scale_both'),
                        css_classes=["display-grid"])
        return file_html(layout, CDN, "MEDIAN SNR")
