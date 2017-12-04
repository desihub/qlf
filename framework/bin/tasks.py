from celery import Celery, chord
from celery.utils.log import get_task_logger
import datetime
import argparse
import celeryconfig
import os
from qlf_models import QLFModels

models = QLFModels()

logger = get_task_logger(__name__)

app = Celery()
app.config_from_object(celeryconfig)

@app.task
def start(data):
    """ Adds initial information about processing in the database. """
    data['pipeline_name'] = 'Quick Look'

    logger.info('Started %s ...' % data.get('pipeline_name'))
    logger.info('Night: %s' % data.get('night'))
    logger.info('Exposure: %s' % str(data.get('expid')))

    data['start'] = datetime.datetime.now().replace(microsecond=0)

    # create process in database and obtain the process id
    process = models.insert_process(data)

    data['process_id'] = process.id
    data['status'] = process.status

    # TODO: ingest configuration file used, this should be done by process
    # self.models.insert_config(process.id)

    logger.info('Process ID: %i' % process.id)
    logger.info('Starting...')

    output_dir = os.path.join(
        'exposures',
        data.get('night'),
        data.get('zfill')
    )

    output_full_dir = os.path.join(
        data.get('desi_spectro_redux'),
        output_dir
    )

    # Make sure output dir is created
    if not os.path.isdir(output_full_dir):
        os.makedirs(output_full_dir)

    logger.info('Output dir: %s' % output_dir)

    data['output_dir'] = output_dir

    runs = list()

    for camera in data.get('cameras'):
        logname = os.path.join(
            data.get('output_dir'),
            "run-%s.log" % camera.get('name')
        )

        camera['logname'] = logname

        logger.info('Output log for camera %s: %s' % (
            camera.get('name'), camera.get('logname')
        ))

        job = models.insert_job(
            process_id=data.get('process_id'),
            camera=camera.get('name'),
            logname=camera.get('logname')
        )

        camera['job_id'] = job.id

        runs.append(parallel_job.s(data, camera))

    jobs_callback = finish.s(data)
    jobs = chord(runs)(jobs_callback)
    logger.info(jobs)
    # job_runs = jobs.apply_async()
    # job_runs.join()

@app.task
def parallel_job(data, camera):
    """ Execute QL Pipeline by camera """

    camera['start'] = datetime.datetime.now().replace(microsecond=0)

    logger.info(
        "Started job %i on exposure %s and camera %s ... " % (
        camera.get('job_id'),
        data.get('expid'),
        camera.get('name')
    ))

    params = argparse.Namespace(
        camera=camera.get('name'), config=data.get('qlconfig'),
        expid=int(data.get('expid')), fullconfig=None,
        mergeQA=False, night=data.get('night'),
        qlf=False, rawdata_dir=data.get('desi_spectro_data'),
        save=None, specprod_dir=data.get('desi_spectro_redux')
    )

    try:
        from desispec.scripts import quicklook
        quicklook.ql_main(params)
        retcode = 0
    except Exception as error:
        retcode = 1
        logger.error(error)

    camera['end'] = datetime.datetime.now().replace(microsecond=0)
    camera['status'] = 0
    camera['duration'] = str(
        camera.get('end') - camera.get('start')
    )

    if retcode < 0:
        camera['status'] = 1
        msg = (
            "Job on exposure %s and camera %s "
            "finished with code %i in %s"
        ) % (
            camera.get('name'),
            data.get('expid'),
            retcode,
            camera.get('duration')
        )
        logger.error(msg)

    logger.info("Finished job %i in %s" % (
        camera.get('job_id'),
        camera.get('duration')
    ))

    return camera

@app.task
def finish(cameras, data):
    """ Finish pipeline. """

    if not isinstance(cameras, list):
        cameras = [cameras]

    print('----> Cameras: ', cameras)

    logger.info('Begin ingestion of results...')
    start_ingestion = datetime.datetime.now().replace(microsecond=0)

    # TODO: refactor?
    camera_failed = 0

    for camera in cameras:

        print(camera)

        output_path = os.path.join(
            data.get('desi_spectro_redux'),
            data.get('output_dir'),
            'ql-*-%s-%s.yaml' % (
                camera.get('name'),
                data.get('zfill')
            )
        )

        models.update_job(
            job_id=camera.get('job_id'),
            end=camera.get('end'),
            start=camera.get('start'),
            status=camera.get('status'),
            output_path=output_path
        )

        if not camera.get('status') == 0:
            camera_failed += 1

    status = 0

    if camera_failed > 0:
        status = 1

    data['status'] = status

    duration_ingestion = str(
        datetime.datetime.now().replace(microsecond=0) - start_ingestion
    )

    logger.info("Results ingestion complete in %s." % duration_ingestion)

    data['end'] = datetime.datetime.now().replace(microsecond=0)

    print('---> DATE: ', data.get('start'))

    data['duration'] = str(data.get('end') - datetime.datetime.strptime('2017-11-09 17:36:54', '%Y-%m-%d %H:%M:%S'))

    logger.info("Process with expID {} completed in {}.".format(
        data.get('expid'),
        data.get('duration')
    ))

    models.update_process(
        process_id=data.get('process_id'),
        end=data.get('end'),
        process_dir=data.get('output_dir'),
        status=data.get('status')
    )


import time

@app.task
def wrapper():

    # to kill all running task
    # result = wrapper.s().apply_async()
    # for x in result.children:
    #     x.revoke(terminate=True)
    #     # or x.revoke(terminate=True)

    callback = create_log.s('Testing')
    header = [add.s(200), add.s(400)]
    chord(header)(callback)

@app.task
def add(x):

    print('Add %i' % x)
    time.sleep(x)
    return {'number': x}

@app.task
def create_log(d, e):

    print('PARAM 1: %s' % str(d))
    print('PARAM 2: %s' % str(e))

    return d, e
