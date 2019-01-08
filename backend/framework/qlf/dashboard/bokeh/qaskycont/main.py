from bokeh.layouts import column

from bokeh.models import ColumnDataSource
from bokeh.models import LinearColorMapper, Range1d
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import Div
from qlf_models import QLFModels
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.plot2d.main import Plot2d

import numpy as np
from bokeh.resources import CDN
from bokeh.embed import file_html


class Skycont:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        gen_info = mergedqa['GENERAL_INFO']
        ra = gen_info['RA']
        dec = gen_info['DEC']
        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
        skycont = check_spectra['METRICS']
        sky = skycont['SKYCONT_FIBER']
        skyfibers = gen_info['SKY_FIBERID']
        nrg = check_spectra['PARAMS']['SKYCONT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['SKYCONT_WARN_RANGE']

        ra_sky = [ra[i] for i in skyfibers]
        dec_sky = [dec[i] for i in skyfibers]

        my_palette = get_palette("viridis")

        skc_tooltips = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">SKY CONT: </span>
                    <span style="font-size: 1vw; color: #515151;">@skycont</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1vw; color: #515151;">@ra</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 1vw; color: #515151;">@dec</span>
                </div>
            </div>
        """
        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        qlf_fiberid = np.arange(0, 500)

        # sky continuum per sky fiber averaged over two continuum regions,
        #  'n' is number of sky fibers

        ra_not, dec_not = [], []
        for i in range(500):
            if i not in skyfibers:
                ra_not.append(ra[i])
                dec_not.append(dec[i])

        source = ColumnDataSource(data={
            'skycont': sky,
            'fiberid': skyfibers,
            'ra': ra_sky,
            'dec': dec_sky
        })

        source_not = ColumnDataSource(data={
            'ra': ra_not,
            'dec': dec_not,
            'skycont': ['']*len(dec_not)
        })

        mapper = LinearColorMapper(palette=my_palette,
                                   low=np.min(sky),
                                   high=np.max(sky),
                                   nan_color='darkgray')

        radius = 0.0165  # 0.013
        radius_hover = 0.02  # 0.015

        # centralize wedges in plots:
        ra_center=0.5*(max(ra)+min(ra))
        dec_center=0.5*(max(dec)+min(dec))
        xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
        yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

        wedge_plot = Plot2d(
            x_range=xrange_wedge,
            y_range=yrange_wedge,
            x_label="RA",
            y_label="DEC",
            tooltip=skc_tooltips,
            title="SKY_CONT",
            width=500,
            height=380,
            yscale="auto"
        ).wedge(
            source,
            x='ra',
            y='dec',
            field='skycont',
            mapper=mapper,
        ).wedge(
            source_not,
            x='ra',
            y='dec',
        ).plot

        taptool = wedge_plot.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        # infos
        info_col = Title().write_description('skycont')

       # Prepare tables
        current_exposures = [check_spectra['METRICS']['SKYCONT']]
        program = gen_info['PROGRAM'].upper()
        reference_exposures = check_spectra['PARAMS']['SKYCONT_' + program + '_REF']
        keynames = ["SKYCONT" for i in range(len(current_exposures))]
        metric = Table().reference_table(keynames, current_exposures, reference_exposures)
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        column(wedge_plot, sizing_mode='scale_both',
                               css_classes=["main-one"]),
                        css_classes=["display-grid"])

        # End of Bokeh Block
        return file_html(layout, CDN, "SKYCONT")
