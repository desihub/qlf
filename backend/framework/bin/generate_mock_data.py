from qlf_models import QLFModels
from copy import copy
import collections
import numpy
import datetime
import random

qlf_models = QLFModels()

FLAVORS = {
    'science': 1.0,
    'flat': 0.1,
    'arc': 0.1
}


def generate_processes_by_exposure(exposure, loop=1):
    """ """

    flavor = exposure.flavor

    process = qlf_models.get_last_process_by_flavor(
        flavor, jobs_isnull=False)

    if not process:
        raise ValueError(
            'There is no process with {} flavor.'.format(flavor)
        )

    process.exposure_id = exposure.exposure_id

    processes = list()

    for item in range(loop):
        print('Starting {} process simulation...'.format(item + 1))
        process.id = None
        tdate = datetime.datetime.now()
        tdate += datetime.timedelta(minutes=random.randint(1, 5))
        process.end = tdate
        process.save()
        print('End {}: process ID {}'.format(item + 1, process.id))
        processes.append(copy(process))

    return processes

def generate_new_exposure(flavor, night):
    """ """

    last_exp = qlf_models.get_last_exposure()
    exposure = qlf_models.get_last_exposure_by_flavor(flavor)

    if not exposure:
        raise ValueError(
            'There is no exposure with {} flavor.'.format(flavor)
        )

    exposure.exposure_id = last_exp.exposure_id + 1
    exposure.night = night
    tdate = datetime.datetime.strptime(night, "%Y%m%d")
    tdate += datetime.timedelta(hours=random.randint(1, 23))
    exposure.dateobs = tdate
    exposure.telra += random.randint(-20, 20)
    exposure.teldec += random.randint(-20, 20)
    exposure.save()

    return exposure

METRICS = {
    'CHECK_SPECTRA': ['FIBER_MAG', 'SNR_MAG_TGT', 'SKYCONT_FIBER', 'DELTAMAG_TGT', 'PEAKCOUNT_FIB', 'PEAKCOUNT', 'DELTAMAG'],
    'CHECK_CCDs': ['BIAS_AMP', 'NOISE_AMP', 'XWSIGMA_FIB', 'NOISE_OVERSCAN_AMP', 'XWSIGMA_AMP', 'XWSIGMA']
}

def generate_jobs_by_process(process):
    """ """

    main_process = qlf_models.get_last_process_by_flavor(
        process.exposure.flavor,
        jobs_isnull=False
    )

    jobs = qlf_models.get_jobs_by_process_id(main_process.id)

    for job in jobs:
        job.id = None
        job.process_id = process.id

        for m in METRICS:
            if m in job.output['TASKS'].keys():
                for item in job.output['TASKS'][m]['METRICS']:
                    if item in METRICS[m]:
                        try:
                            out = job.output['TASKS'][m]['METRICS'][item]
                            out = simulate_output(out, -6.0, 6.0)
                            job.output['TASKS'][m]['METRICS'][item] = out
                        except:
                            print('Error in {}/{} simulation.'.format(m, item))

        job.output = simulate_output(job.output)
        job.save()


def simulate_output(output, ini=-6.0, end=6.0):
    """ """

    def update(data):
        if type(data) == numpy.ndarray:
            data = data.tolist()
        if isinstance(data, list):
            for item in data:
                data[data.index(item)] = update(item)
        if isinstance(data, dict):
            for item in data:
                data[item] = update(data[item])
        if isinstance(data, (int, float,)):
            data += random.uniform(ini, end)

        return data

    return update(output)


def simulate(night_base, num_days=30, num_exp=40):

    base = datetime.datetime.strptime(night_base, "%Y%m%d")

    flavors = list(qlf_models.get_flavors())
    weights = list()

    for idx, val in enumerate(flavors):
        weights.append(FLAVORS[val]) 

    print(flavors)
    print(weights)

    for x in range(0, num_days):
        nbase = base + datetime.timedelta(days=x)
        nbase = nbase.strftime("%Y%m%d")

        for exp in range(0, num_exp):
            flavor = random.choices(flavors, weights)
            new_exposure = generate_new_exposure(flavor.pop(), nbase)
            new_processes = generate_processes_by_exposure(new_exposure)

            for process in new_processes:
                generate_jobs_by_process(process)


simulate('20181001', num_days=2, num_exp=4)
