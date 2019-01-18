from bokeh.layouts import column

from bokeh.models.widgets import Div

from bokeh.models import ColumnDataSource
from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.plot2d.main import Plot2d

import numpy as np

from qlf_models import QLFModels
from dashboard.models import Job, Process, Fibermap

from bokeh.resources import CDN
from bokeh.embed import file_html


class Integ:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(
            self.selected_process_id, cam)

        gen_info = mergedqa['GENERAL_INFO']

        check_spectra = mergedqa['TASKS']['CHECK_SPECTRA']
        std_fiberid = mergedqa['GENERAL_INFO']['STAR_FIBERID']
        nrg = check_spectra['PARAMS']['DELTAMAG_TGT_NORMAL_RANGE']
        wrg = check_spectra['PARAMS']['DELTAMAG_TGT_WARN_RANGE']
        fiber_mag = np.array(mergedqa['GENERAL_INFO']['FIBER_MAGS'])

        if 'b' in cam:
            arm_id=0
        elif 'r' in cam:
            arm_id=1
        else:
            arm_id=2

        fiber_mag = fiber_mag[arm_id]#.flatten()

        tooltip = """ 
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">INTEG: </span>
                    <span style="font-size: 1vw; color: #515151;">@integ</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@x</span>
                </div>
            </div>
                """

        source = ColumnDataSource(
            data={
                'integ':  [i if i >-999 else np.nan for i in fiber_mag],
                'x': np.arange(len(fiber_mag)),
            }
        )
        print(len(fiber_mag))
        yrange = [0, 1.1*max(fiber_mag)]

        fiber_hist = Plot2d(
            yrange,
            x_label="Fibers",
            y_label="Integral (counts)",
            tooltip=tooltip,
            title="",
            width=600,
            height=400,
            yscale="auto",
            hover_mode="vline",
        ).vbar(
            source,
            y="integ",
        )

        info_col = Title().write_description('integ')

        # Reading obj_type
        process_id = self.selected_process_id
        process = Process.objects.get(pk=process_id)
        joblist = [entry.camera.camera for entry in Job.objects.filter(
            process_id=process_id)]
        exposure = process.exposure
        fmap = Fibermap.objects.filter(exposure=exposure).last()
        otype_tile = fmap.objtype

        objlist = sorted(set(otype_tile))
        if 'SKY' in objlist:
            objlist.remove('SKY')


        # Prepare tables
        current_exposures = check_spectra['METRICS']['DELTAMAG_TGT']
        program = gen_info['PROGRAM'].upper()
        reference_exposures = check_spectra['PARAMS']['DELTAMAG_TGT_' + program  + '_REF']
        keynames = ["DELTAMAG_TGT" + " ({})".format(i) for i in objlist]
        metric = Table().reference_table(keynames, current_exposures, reference_exposures)
        alert = Table().alert_table(nrg, wrg)

        layout = column(info_col, Div(),
                        metric,
                        alert,
                        column(fiber_hist, sizing_mode='scale_both', css_classes=["main-one"]),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "INTEG")
