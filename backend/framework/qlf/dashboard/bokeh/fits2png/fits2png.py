import sys
import os
from astropy.io import fits
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from util import get_config
from bokeh.models import LogColorMapper
import numpy as np

cfg = get_config()

desi_spectro_data = cfg.get("namespace", "desi_spectro_data")
desi_spectro_redux = cfg.get("namespace", "desi_spectro_redux")


class Fits2png:
    def __init__(self, cam, processing, night, exposure):
        self.cam = cam
        self.processing = processing
        self.night = night
        self.exposure = exposure

    def convert_fits2png(self):
        exp_zfill = str(self.exposure).zfill(8)

        if self.processing == 'raw':
            f = '{}/{}/desi-{}.fits.fz'.format(desi_spectro_data,
                                               self.night, exp_zfill)
        elif self.processing == 'reduced':
            f = '{}/exposures/{}/{}/sframe-{}-{}.fits'.format(
                desi_spectro_redux, self.night, exp_zfill, self.cam, exp_zfill)
        else:
            return 'Invalid processing option'

        try:
            img = fits.open(f)
        except FileNotFoundError:
            return 'File not found'

        if self.processing == 'raw':
            offset = 0
            if self.cam[0] == 'r':
                offset = 10
            if self.cam[0] == 'z':
                offset = 20
            img_data = img[offset+int(self.cam[1])+1]
        else:
            img_data = img[0]
        p = figure(
            x_range=(0, img_data.data.shape[0]-1), y_range=(0, img_data.data.shape[1]-1))

        low = np.amin(img_data.data)
        high = np.amax(img_data.data)
        color_mapper = LogColorMapper(
            palette="Greys256", low=low, high=high)
        p.image(image=[img_data.data], x=0, y=0, dw=img_data.data.shape[0] -
                1, dh=img_data.data.shape[1]-1, color_mapper=color_mapper)
        return file_html(p, CDN, "png")
