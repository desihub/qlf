#!/usr/bin/env python

import os
import sys
import yaml
import glob
import numpy
import django
import math
import argparse
import concurrent.futures

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

django.setup()

from dashboard.models import Job, QA


def update_job(job_id, end, status, output_path):
    """ Updates job with execution results. """

    try:
        Job.objects.filter(id=job_id).update(
            end=end,
            status=status
        )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            {executor.submit(parallel_ingestion, product, job_id): product for product in glob.glob(output_path)}

        #qas = list()

        #for product in glob.glob(output_path):
        #    qa = create_qa_bulk(product, job_id)
        #    if qa:
        #        qas.append(qa)

        #QA.objects.bulk_create(qas)

        print('Job {} updated.'.format(job_id))
    except Exception as err:
        print(err)
        print('Job {} failed.'.format(job_id))

def create_qa_bulk(product, job_id):
    qa = yaml.load(open(product, 'r'))
    name = os.path.basename(product)

    if 'PANAME' in qa and 'METRICS' in qa and 'PARAMS' in qa:
        paname = qa['PANAME']
        metrics = jsonify(qa['METRICS'])
        params = jsonify(qa['PARAMS'])

        return QA(
            name=name,
            description='',
            paname=paname,
            metrics=metrics,
            params=params,
            job_id=job_id
        )

    return None

def parallel_ingestion(product, job_id):
    qa = yaml.load(open(product, 'r'))
    name = os.path.basename(product)

    if 'PANAME' in qa and 'METRICS' in qa and 'PARAMS' in qa:
        paname = qa['PANAME']
        metrics = jsonify(qa['METRICS'])
        params = jsonify(qa['PARAMS'])

        print("Ingesting %s" % name)
        print("Type: {}".format(str(type(qa['METRICS']))))
        insert_qa(name, paname, metrics, params, job_id)


def insert_qa(name, paname, metrics, params, job_id, force=False):
    """ Inserts or updates qa table """

    if not QA.objects.filter(name=name):
        # Register for QA results for the first time
        qa = QA(
            name=name,
            description='',
            paname=paname,
            metrics=metrics,
            params=params,
            job_id=job_id
        )
        qa.save()
    elif force:
        # Overwrite QA results
        QA.objects.filter(name=name).update(
            job_id=job_id,
            description='',
            paname=paname,
            metrics=metrics,
            params=params,
        )
    else:
        print(
            "{} results already registered. "
            "Use --force to overwrite.".format(name)
        )

def jsonify(data):
    """ Make a dictionary with numpy arrays JSON serializable """

    for key in data:
        if type(data[key]) == numpy.ndarray:
            data[key] = data[key].tolist()

        if isinstance(data[key], list):
            data[key] = [0 if isinstance(x, float) and math.isnan(x) else x for x in data[key]]

    return data



parser = argparse.ArgumentParser()

parser.add_argument("job_id", help="Job ID")
parser.add_argument("end", help="Processing end date")
parser.add_argument("status", help="Job status")
parser.add_argument("output_dir", help="Products directory")

args = parser.parse_args()

update_job(args.job_id, args.end, args.status, args.output_dir)
