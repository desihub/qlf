from qlf_models import QLFModels
from migrate_jobs_outputs import migrate_job_outputs
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

METRICS = {
    'CHECK_SPECTRA': [
        'FIBER_MAG', 'SNR_MAG_TGT', 'SKYCONT_FIBER', 'PEAKCOUNT',
        'PEAKCOUNT_FIB', 'DELTAMAG_TGT' , 'DELTAMAG'
    ],
    'CHECK_CCDs': [
        'BIAS_AMP', 'NOISE_AMP', 'XWSIGMA_FIB',
        'NOISE_OVERSCAN_AMP', 'XWSIGMA_AMP', 'XWSIGMA'
    ]
}


def generate_processes_by_exposure(exposure):
    """ Creates a simulated process based on an exposure.
    
    Arguments:
        exposure {object} -- Exposure model
    
    Raises:
        ValueError -- returns when there is no processing
        with a respective exposure.
    
    Returns:
        object -- Process model
    """

    flavor = exposure.flavor

    process = qlf_models.get_last_process_by_flavor(
        flavor, jobs_isnull=False)

    if not process:
        raise ValueError(
            'There is no process with {} flavor.'.format(flavor)
        )

    process.exposure_id = exposure.exposure_id

    process.id = None
    tdate = datetime.datetime.now()
    tdate += datetime.timedelta(minutes=random.randint(1, 5))
    process.end = tdate
    process.save()
     
    return process


def generate_new_exposure(flavor, night):
    """ Creates a simulated exposure.
    
    Arguments:
        flavor {str} -- Flavor (ex: 'science', 'flat' or 'arc')
        night {str} -- Night simlulated (ex: 20190101)
    
    Raises:
        ValueError -- Returns when there is no exposure with 
        a respective flavor.
    
    Returns:
        object -- Exposure model
    """


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

    if exposure.telra or exposure.telra == 0:
        exposure.telra = random.randint(0, 360)

    if exposure.teldec or exposure.teldec == 0:
        exposure.teldec = random.randint(-20, 90)

    exposure.save()

    fibermap = qlf_models.get_last_fibermap_by_flavor(flavor)
    fibermap.pk = fibermap.pk+1
    fibermap.exposure = exposure
    fibermap.save()

    return exposure


def generate_jobs_by_process(process):
    """ Creates simulated jobs based on a process.
    
    Arguments:
        process {object} -- Process model
    """


    main_process = qlf_models.get_last_process_by_flavor(
        process.exposure.flavor,
        jobs_isnull=False
    )

    jobs = qlf_models.get_jobs_by_process_id(main_process.id)

    for job in jobs:
        job.id = None
        job.process_id = process.id

        # Modifying for the metrics that I 
        for m in METRICS:
            if m in job.output['TASKS'].keys():
                for item in job.output['TASKS'][m]['METRICS']:
                    if item in METRICS[m]:
                        try:
                            out = job.output['TASKS'][m]['METRICS'][item]
                            out = simulate_output(out, -2.0, 2.0)
                            job.output['TASKS'][m]['METRICS'][item] = out
                        except:
                            print('Error in {}/{} simulation.'.format(m, item))

        # 
        # job.output = simulate_output(job.output)
        job.save()


def simulate_output(output, ini=-6.0, end=6.0):
    """ Simulates random values in QA output.
    
    Arguments:
        output {dict} -- QA output
    
    Keyword Arguments:
        ini {float} -- start range random (default: {-6.0})
        end {float} -- end range random (default: {6.0})
    
    Returns:
        dict -- QA output with simulated values 
    """

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


def simulate(night_base, num_days=3, num_exp=40):
    """ Simulates the nights processing.
    
    Arguments:
        night_base {str} -- Night initial (ex: 20190101)
    
    Keyword Arguments:
        num_days {int} -- Number of simulated nights (default: {3})
        num_exp {int} -- Number of exposures per night (default: {40})
    """


    base = datetime.datetime.strptime(night_base, "%Y%m%d")

    flavors = list(qlf_models.get_flavors())
    weights = list()

    for idx, val in enumerate(flavors):
        weights.append(FLAVORS[val]) 

    for x in range(0, num_days):
        nbase = base + datetime.timedelta(days=x)
        nbase = nbase.strftime("%Y%m%d")

        for exp in range(0, num_exp):
            flavor = random.choices(flavors, weights)
            new_exposure = generate_new_exposure(flavor.pop(), nbase)
            process = generate_processes_by_exposure(new_exposure)
            generate_jobs_by_process(process)
    migrate_job_outputs()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("night", help="Simulation start date. ex: 20180101")
    parser.add_argument("--days", help="Number of simulated nights", type=int, default=3)
    parser.add_argument("--exps", help="Number of exposures per night", type=int, default=40)

    args = parser.parse_args()

    basenight = args.night
    num_days = args.days  
    num_exp = args.exps

    simulate(basenight, num_days=num_days, num_exp=num_exp)
