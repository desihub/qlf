import logging
import configparser
import os

logger = logging.getLogger()

qlf_root = os.getenv('QLF_ROOT')

if not qlf_root:
    raise ValueError('QLF_ROOT not define.')


def get_config(config_path=None):
    """ """

    if not config_path:
        config_path = os.path.join(
            qlf_root,
            "framework/config/qlf.cfg"
        )

    cfg = configparser.ConfigParser()
    cfg.read(config_path)

    section = 'environment'

    if not cfg.has_section(section):
        cfg.add_section(section)

    cfg.set(section, 'qlf_root', qlf_root)

    return cfg
