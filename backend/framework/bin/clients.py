import logging
import Pyro4
import os
from qlf_interface import QLFInterface

log = logging.getLogger()

EXPOSURE_MONITORING_NS = os.environ.get('EXPOSURE_MONITORING_NS', 'exposure.monitoring')
EXPOSURE_GENERATOR_NS = os.environ.get('EXPOSURE_GENERATOR_NS', 'exposure.generator')
PYRO_HOST = os.environ.get('PYRO_HOST', 'localhost')
PYRO_PORT = str(os.environ.get('PYRO_PORT', 50006))
ICS_NAMESPACE = os.environ.get('ICS_DAEMON_NS', 'ICSDaemon')
ICS_HOST = os.environ.get('ICS_HOST', 'localhost')
ICS_PORT = str(os.environ.get('ICS_PORT', 50006))

EXPOSURE_MONITORING = 'PYRO:{}@{}:{}'.format(
    EXPOSURE_MONITORING_NS,
    PYRO_HOST,
    PYRO_PORT
)

EXPOSURE_GENERATOR = 'PYRO:{}@{}:{}'.format(
    EXPOSURE_GENERATOR_NS,
    PYRO_HOST,
    PYRO_PORT
)

ICS_DAEMON = 'PYRO:{}@{}:{}'.format(
    ICS_NAMESPACE,
    ICS_HOST,
    ICS_PORT
)


def get_exposure_generator():
    """ """
    return Pyro4.Proxy(EXPOSURE_GENERATOR)


def get_exposure_monitoring():
    """ """
    return Pyro4.Proxy(EXPOSURE_MONITORING)


def get_ics_daemon():
    """ """
    return Pyro4.Proxy(ICS_DAEMON)


def get_qlf_interface():
    """ """
    return QLFInterface()
