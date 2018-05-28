import configparser
import os
from qlf_models import QLFModels


class QLFConfiguration:
    def __init__(self):
        qlf_root = os.getenv('QLF_ROOT')
        self.cfg = configparser.ConfigParser()
        self.cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
        self.configuration = self.get_last_configuration()

    def get_current_configuration(self):
        return self.configuration

    def set_current_configuration(self, configuration):
        if configuration == 'reset':
            self.configuration = self.get_default_configuration()
        else:
            self.configuration = configuration

    def get_default_configuration(self):
        configuration = dict(
            base_exposures_path=self.cfg.get("namespace", "base_exposures_path"),
            min_interval=self.cfg.get("main", "min_interval"),
            max_interval=self.cfg.get("main", "max_interval"),
            allowed_delay=self.cfg.get("main", "allowed_delay"),
            max_exposures=self.cfg.get("main", "max_exposures"),
            logfile=self.cfg.get("main", "logfile"),
            loglevel=self.cfg.get("main", "loglevel"),
            logpipeline=self.cfg.get("main", "logpipeline"),
            qlconfig=self.cfg.get("main", "qlconfig"),
            night=self.cfg.get("data", "night"),
            exposures=self.cfg.get("data", "exposures"),
            arms=self.cfg.get("data", "arms"),
            spectrographs=self.cfg.get("data", "spectrographs"),
            desi_spectro_data=self.cfg.get("namespace", "desi_spectro_data"),
            desi_spectro_redux=self.cfg.get("namespace", "desi_spectro_redux")
        )

        return configuration

    def get_last_configuration(self):
        try:
            configuration = QLFModels().get_last_configuration()
        except:
            configuration = self.get_default_configuration()
            configuration = QLFModels().insert_config("default", configuration)

        return configuration
