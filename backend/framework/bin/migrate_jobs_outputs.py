from qlf_models import QLFModels
import sys

qlf_models = QLFModels()

metrics = {
    'skybrightness': {
        'display': 'SKY BRIGHTNESS',
        'path': 'TASKS->CHECK_SPECTRA->METRICS->PEAKCOUNT'
    },
    'airmass': {
        'display': 'AIRMASS',
        'path': 'GENERAL_INFO->AIRMASS'
    },
    'bias': {
        'display': 'BIAS',
        'path': 'TASKS->CHECK_CCDs->METRICS->BIAS_AMP'
    },
    'noise': {
        'display': 'NOISE',
        'path': 'TASKS->CHECK_CCDs->METRICS->NOISE_AMP'
    },
}

def migrate_job_outputs():
    qlf_models.migrate_outputs(metrics)


if __name__ == "__main__":
    migrate_job_outputs()
