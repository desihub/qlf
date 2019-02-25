from bokeh.layouts import column

from bokeh.models.widgets import Div

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.patch.main import Patch

from qlf_models import QLFModels

from bokeh.resources import CDN
from bokeh.embed import file_html


class RMS:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        check_ccds = mergedqa['TASKS']['CHECK_CCDs']
        getrms = check_ccds['METRICS']

        nrg = check_ccds['PARAMS']['NOISE_AMP_NORMAL_RANGE']
        wrg = check_ccds['PARAMS']['NOISE_AMP_WARN_RANGE']
        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        refexp = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['NOISE_AMP' +
                                                           program_prefix+'_REF']

        # amp 1
        p = Patch().plot_amp(
            dz=getrms["NOISE_AMP"],
            refexp=refexp,
            name="NOISE_AMP",
            description="NOISE(photon counts)",
            wrg=wrg
        )

        p_stat = Patch().plot_amp(
            dz=getrms["NOISE_AMP"],
            refexp=refexp,
            name="NOISE_AMP (STATUS)",
            description="NOISE (photon counts)",
            wrg=wrg,
            nrg=nrg,
            status_plot=True
        )
        # amp 2
        p2 = Patch().plot_amp(
            dz=getrms["NOISE_OVERSCAN_AMP"],
            refexp=refexp,
            name="NOISE_OVERSCAN_AMP",
            description="NOISE Overscan (photon counts)",
            wrg=wrg
        )

        p2_stat = Patch().plot_amp(
            dz=getrms["NOISE_OVERSCAN_AMP"],
            refexp=refexp,
            name="NOISE_OVERSCAN_AMP (STATUS)",
            description="NOISE Overscan (photon counts)",
            wrg=wrg,
            nrg=nrg,
            status_plot=True
        )

        info_col = Title().write_description('getrms')

        # Prepare tables
        current_exposures = check_ccds['METRICS']['NOISE_AMP']
        gen_info = mergedqa['GENERAL_INFO']
        flavor = mergedqa["FLAVOR"]
        if flavor == 'science':
            program = gen_info['PROGRAM'].upper()
            reference_exposures = check_ccds['PARAMS']['LITFRAC_AMP_' +
                                                       program + '_REF']
        else:
            reference_exposures = check_ccds['PARAMS']['LITFRAC_AMP_REF']
        keynames = ["NOISE_AMP" for i in range(len(current_exposures))]
        table = Table().single_table(keynames, current_exposures, reference_exposures, nrg, wrg)

        layout = column(info_col, Div(),
                        table, Div(),
                        column(p,  sizing_mode='scale_both'),
                        column(p2, sizing_mode='scale_both'),
                        column(p_stat,  sizing_mode='scale_both'),
                        column(p2_stat,  sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "GETRMS")
