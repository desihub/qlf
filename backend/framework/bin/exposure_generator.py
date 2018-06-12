import datetime
import os
import json
import random
import re
import shutil
import time
from multiprocessing import Manager, Process

import astropy.io.fits

from log import get_logger
from qlf_models import QLFModels
from util import get_config, extract_exposure_data


cfg = get_config()
qlf_root = cfg.get("environment", "qlf_root")

log = get_logger(
    "exposure.generator",
    os.path.join(qlf_root, "logs", "exposure_generator.log")
)

spectro_data = cfg.get("namespace", "desi_spectro_data")
spectro_redux = cfg.get("namespace", "desi_spectro_redux")
base_exposures_path = cfg.get("namespace", "base_exposures_path")

# TODO: verify desispec.io.findfile function to get the files correctly
fiberflat_path = os.path.join(base_exposures_path, "fiberflat")
psf_path = os.path.join(base_exposures_path, "psf")

min_interval = cfg.getint("main", "min_interval")
max_interval = cfg.getint("main", "max_interval")
max_exposures_per_night = cfg.getint("main", "max_exposures")
max_nights = cfg.getint("main", "max_nights")


class ExposureGenerator(Process):

    def __init__(self):
        super().__init__()
        self.__last_exposure = Manager().dict()
        self.__base_exposure = 0
        self.__print_vars()

    def run(self):
        last_registered = QLFModels().get_last_exposure()

        if last_registered:
            last_date_obs = last_registered.dateobs
            last_exposure_id = last_registered.pk
        else:
            last_date_obs = datetime.datetime.utcnow()
            last_exposure_id = 2

        for x in self.__xrange(1, max_nights):
            new_date_obs = last_date_obs + datetime.timedelta(days=x)
            night = self.__format_night(new_date_obs)
            log.info("Night {} starting".format(night))

            for y in self.__xrange(1, max_exposures_per_night):
                exposure_id = last_exposure_id + y
                dateobs = self.__datetime_to_str(new_date_obs)

                log.info("-> Exposure ID {} generating".format(
                    exposure_id
                ))

                last_exposure = self.generate_exposure(
                    exposure_id, dateobs, night)

                self.__last_exposure.update(last_exposure)

                if y == max_exposures_per_night and x == max_nights:
                    continue

                minutes = random.randint(min_interval, max_interval)
                log.info("Next generation in {} minutes...".format(minutes))

                time.sleep(minutes * 60)

            last_exposure_id += max_exposures_per_night

    def __get_random_base_exposure(self):
        """ """

        if not os.path.exists(base_exposures_path):
            log.error("Directory does not exist: {}".format(
                base_exposures_path))
            raise OSError

        exposures_list = re.findall(
            r"desi-(\d+).fits.fz",
            ''.join(os.listdir(base_exposures_path))
        )

        return random.choice(exposures_list)

    def get_last_exposure(self):
        return Manager().dict(self.__last_exposure)

    def generate_exposure(self, exposure_id, date_obs, night):

        self.__base_exposure = self.__get_random_base_exposure()

        log.info("Base exposure: {}".format(self.__base_exposure))

        exposure_zfill = str(exposure_id).zfill(8)

        self.__gen_desi_file(exposure_zfill, night, date_obs)
        self.__gen_fibermap_file(exposure_zfill, night, date_obs)
        self.__gen_fiberflat_folder(night)
        self.__gen_psfboot_folder(night)

        return extract_exposure_data(exposure_id, night)

        # expo_name = "desi-{}.fits.fz".format(exposure_zfill)

        # file_path = os.path.join(spectro_path, night, expo_name)

        # try:
        #     hdr = astropy.io.fits.getheader(file_path)
        # except Exception as err:
        #     log.error("Error to load fits file: %s" % err)
        #     return {}

        # return {
        #     "exposure_id": exposure_id,
        #     "dateobs": self.__date_obs(gen_time),
        #     "night": night,
        #     "zfill": exposure_zfill,
        #     "desi_spectro_data": spectro_path,
        #     "desi_spectro_redux": spectro_redux,
        #     'telra': hdr.get('telra', None),
        #     'teldec': hdr.get('teldec', None),
        #     'tile': hdr.get('tileid', None),
        #     'flavor': hdr.get('flavor', None),
        #     'program': hdr.get('program', None),
        #     'airmass': hdr.get('airmass', None),
        #     'exptime': hdr.get('exptime', None),
        #     'time': datetime.datetime.utcnow()
        # }

    def __gen_desi_file(self, exposure_id, night, date_obs):
        dest = os.path.join(spectro_data, night)
        self.__ensure_dir(dest)
        src_file = os.path.join(
            base_exposures_path,
            "desi-{}.fits.fz".format(self.__base_exposure)
        )
        dest_file = os.path.join(dest, "desi-{}.fits.fz".format(exposure_id))
        shutil.copy(src_file, dest_file)
        self.__update_fitsfile_metadata(
            dest_file, exposure_id, night, date_obs)

    def __gen_fibermap_file(self, exposure_id, night, date_obs):
        dest = os.path.join(spectro_data, night)
        self.__ensure_dir(dest)
        src_file = os.path.join(
            base_exposures_path,
            "fibermap-{}.fits".format(self.__base_exposure)
        )
        dest_file = os.path.join(dest, "fibermap-{}.fits".format(exposure_id))
        shutil.copy(src_file, dest_file)
        self.__update_fitsfile_metadata(
            dest_file, exposure_id, night, date_obs)

    def __update_fitsfile_metadata(self, exp_file, exposure_id,
                                   night, date_obs):
        hdulist = astropy.io.fits.open(exp_file, mode="update")

        for hduid in range(0, len(hdulist)):
            if "EXPID" in hdulist[hduid].header:
                hdulist[hduid].header["EXPID"] = int(exposure_id)
            if "DATE-OBS" in hdulist[hduid].header:
                hdulist[hduid].header["DATE-OBS"] = date_obs
            if "NIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["NIGHT"] = night
            if "ARCNIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["ARCNIGHT"] = night
            if "FLANIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["FLANIGHT"] = night

        hdulist.flush()
        hdulist.close()

    def __gen_fiberflat_folder(self, night):
        """ """

        dest = os.path.join(spectro_redux, "exposures", night)
        self.__ensure_dir(dest)
        dest = os.path.join(dest, "00000001")

        if not os.path.islink(dest):
            os.symlink(fiberflat_path, dest)

    def __gen_psfboot_folder(self, night):
        """ """

        dest = os.path.join(spectro_redux, "exposures", night)
        self.__ensure_dir(dest)
        dest = os.path.join(dest, "00000000")

        if not os.path.islink(dest):
            os.symlink(psf_path, dest)

    @staticmethod
    def __datetime_to_str(date_obj):
        return date_obj.strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def __str_to_datetime(date_str):
        return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def __format_night(new_date):
        return new_date.strftime("%Y%m%d")

    @staticmethod
    def __ensure_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def __xrange(start, stop, step=1):
        while start <= stop:
            yield start
            start += step

    @staticmethod
    def __print_vars():
        log.info("min_interval:      {}".format(min_interval))
        log.info("max_interval:      {}".format(max_interval))
        log.info("max_nights:        {}".format(max_nights))
        log.info("max_exposures:     {}".format(max_exposures_per_night))
        log.info("spectro_data:      {}".format(spectro_data))
        log.info("spectro_redux:     {}".format(spectro_redux))
        log.info("base_exposures:    {}".format(base_exposures_path))


if __name__ == "__main__":
    log.info('Start Exposure Generator...')
    generator = ExposureGenerator()
    generator.start()
    generator.join()
