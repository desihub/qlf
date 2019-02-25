from bokeh.layouts import column

from bokeh.models.widgets import Div

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.patch.main import Patch

from qlf_models import QLFModels

from bokeh.resources import CDN
from bokeh.embed import file_html


class Countpix:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        gen_info = mergedqa['GENERAL_INFO']
        flavor = mergedqa["FLAVOR"]
        check_ccds = mergedqa['TASKS']['CHECK_CCDs']
        tests = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']

        nrg = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP_NORMAL_RANGE']
        wrg = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP_WARN_RANGE']
        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        refexp = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['LITFRAC_AMP' +
                                                           program_prefix+'_REF']

        # PATCH
        p = Patch().plot_amp(
            dz=check_ccds['METRICS']["LITFRAC_AMP"],
            refexp=refexp,
            name="LITFRAC_AMP",
            description="Average bias value (photon counts)",
            wrg=wrg
        )

        p_status = Patch().plot_amp(
            dz=check_ccds['METRICS']["LITFRAC_AMP"],
            refexp=refexp,
            name="LITFRAC_AMP (STATUS)",
            description="Average bias value (photon counts)",
            wrg=wrg,
            nrg=nrg,
            status_plot=True
        )

        # infos
        info_col = Title().write_description('countpix')

        # Prepare tables
        current_exposures = check_ccds['METRICS']['LITFRAC_AMP']
        if flavor == 'science':
            program = gen_info['PROGRAM'].upper()
            reference_exposures = check_ccds['PARAMS']['LITFRAC_AMP_' +
                                                         program + '_REF']
        else:
            reference_exposures = check_ccds['PARAMS']['LITFRAC_AMP_REF']
        keynames = ["LITFRAC_AMP" for i in range(len(current_exposures))]
        table = Table().single_table(keynames, current_exposures, reference_exposures, nrg, wrg)

        layout = column(info_col, Div(),
                        table, Div(),
                        column(p, sizing_mode='scale_both'),#css_classes=["main-one"]),
                        column(p_status, sizing_mode='scale_both'),
                        css_classes=["display-grid"])

        return file_html(layout, CDN, "Countpix")
