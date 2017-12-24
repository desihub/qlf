from django.shortcuts import render
from django.http import HttpResponse
from channels import Group
import subprocess, fcntl, os, json
import configparser
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def open_file(filename):
    qlf_root = os.getenv('QLF_ROOT')
    cfg = configparser.ConfigParser()

    try:
        cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
        desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    except Exception as error:
        logger.error(error)
        logger.error("Error reading  %s/framework/config/qlf.cfg" % qlf_root)
    try:
        logfile = cfg.get('main', filename)
        return logfile

    except Exception as e:
        logger.warn(e)

def send_message(request):
    logfile = open_file('logfile')
    file = open(logfile, "r")
    lines = file.readlines()
    Group("monitor").send({
        "text": json.dumps({
            "lines": lines,
        })
    })
    # open('/app/debug.log', 'w').write(str("x\n"))
    return HttpResponse(status=201)
