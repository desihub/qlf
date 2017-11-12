from django.shortcuts import render
from django.http import HttpResponse
from channels import Group
import subprocess, fcntl, os
import configparser
import logging
from django.conf import settings

def open_stream(filename):
    qlf_root = os.getenv('QLF_ROOT')
    cfg = configparser.ConfigParser()

    try:
        cfg.read('%s/qlf/config/qlf.cfg' % qlf_root)
        desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    except Exception as error:
        logger.error(error)
        logger.error("Error reading  %s/qlf/config/qlf.cfg" % qlf_root)
    try:
        logfile = cfg.get('main', filename)
        return logfile

    except Exception as e:
        logger.warn(e)

def send_message(request):
    Group("monitor").send({
        "text": 'aqui',
    })
    print('abcas')
    logfile = open_stream('logfile')
    file = open(logfile, "r")
    lines = file.readlines()
    for line in lines:
      open('/app/debug.log', 'w').write(str(line))
      Group("monitor").send({
          "text": line,
      })
    return HttpResponse(status=201)
