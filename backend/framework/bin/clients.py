import logging
import Pyro4
import os
from qlf_interface import QLFInterface

log = logging.getLogger()

EXPOSURE_MONITORING_NS = os.environ.get('EXPOSURE_MONITORING_NS', 'exposure.monitoring')
EXPOSURE_GENERATOR_NS = os.environ.get('EXPOSURE_GENERATOR_NS', 'exposure.generator')
PYRO_HOST = os.environ.get('PYRO_HOST', 'localhost')
PYRO_PORT = str(os.environ.get('PYRO_PORT', 56006))

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


def get_exposure_generator():
    """ """
    return Pyro4.Proxy(EXPOSURE_GENERATOR)


def get_exposure_monitoring():
    """ """
    return Pyro4.Proxy(EXPOSURE_MONITORING)

def get_qlf_interface():
    """ """
    return QLFInterface()
