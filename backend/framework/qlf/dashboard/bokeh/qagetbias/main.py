from bokeh.layouts import column

from bokeh.models.widgets import Div

from qlf_models import QLFModels

from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.patch.main import Patch

from bokeh.resources import CDN
from bokeh.embed import file_html


class Bias:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)
        check_ccds = mergedqa['TASKS']['CHECK_CCDs']
        getbias = check_ccds['METRICS']

        nrg = check_ccds['PARAMS']['BIAS_AMP_NORMAL_RANGE']
        wrg = check_ccds['PARAMS']['BIAS_AMP_WARN_RANGE']
        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        refexp = mergedqa['TASKS']['CHECK_CCDs']['PARAMS']['BIAS_AMP' +
                                                           program_prefix+'_REF']

        # PATCH
        p = Patch().plot_amp(
            dz=getbias["BIAS_AMP"],
            refexp=refexp,
            name="BIAS_AMP",
            description="Average bias value per Amp (photon counts)",
            wrg=wrg
        )

        # INFO TABLES:
        info_col = Title().write_description('getbias')

        # Prepare tables
        current_exposures = check_ccds['METRICS']['BIAS_AMP']
        gen_info = mergedqa['GENERAL_INFO']
        flavor = mergedqa["FLAVOR"]
        if flavor == 'science':
            program = gen_info['PROGRAM'].upper()
            reference_exposures = check_ccds['PARAMS']['BIAS_AMP_' +
                                                       program + '_REF']
        else:
            reference_exposures = check_ccds['PARAMS']['BIAS_AMP_REF']
        keynames = ["BIAS_AMP" for i in range(len(current_exposures))]
        metric = Table().reference_table(keynames, current_exposures, reference_exposures)
        alert = Table().alert_table(nrg,wrg)

        layout = column(info_col, Div(),
                        metric, alert,
                        column(p, sizing_mode='scale_both', css_classes=["main-one"]),
                        css_classes=["display-grid"])


        return file_html(layout, CDN, "GETBIAS")
