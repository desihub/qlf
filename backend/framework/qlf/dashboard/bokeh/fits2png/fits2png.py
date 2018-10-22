import os
from astropy.io import fits
from bokeh.plotting import Figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import LogColorMapper, ColorMapper
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')
desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')


class Fits2png:
    def __init__(self, cam, processing, night, exposure):
        self.cam = cam
        self.processing = processing
        self.night = night
        self.exposure = exposure

    def convert_fits2png(self):
        # f0 = open('dbg2','w'); import time; t0=time.time()
        exp_zfill = str(self.exposure).zfill(8)

        if self.processing == 'raw':
            f = '{}/{}/{}/desi-{}.fits.fz'.format(desi_spectro_data,
                                                  self.night, exp_zfill,
                                                  exp_zfill)
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
            low = np.amin(img_data.data)
            high = np.amax(img_data.data)
            color_mapper = LogColorMapper(
                palette="Greys256", low=low, high=high)
            p = Figure(
                x_range=(0, img_data.data.shape[0]-1), y_range=(0, img_data.data.shape[1]-1))
            p.image(image=[img_data.data], x=0, y=0, dw=img_data.data.shape[0] -
                    1, dh=img_data.data.shape[1]-1, color_mapper=color_mapper)
        else:
            # img_data = img[1]
            # p = Figure(
            #     x_range=(0, img_data.data.shape[0]-1), y_range=(0, img_data.data.shape[1]-1))
            # p.image(image=[img_data.data], x=0, y=0, dw=img_data.data.shape[0] -
            #         1, dh=img_data.data.shape[1]-1, palette="Greys256")

            img_data = img[1].data

            if np.amin(img_data)==0: min=np.amax(img_data)/1.e4
            else: min=np.amin(img_data)

            # f0.write(str(np.amin(img_data)) + ' vmax= ' +str(np.amax(img_data)))
            plt.figure(figsize=(15,5))

            plt.imshow(img_data, cmap='gray', 
                 norm=LogNorm(vmin= min, vmax=np.amax(img_data)))
            plt.tight_layout()
            ofn='{}/exposures/{}/{}/spec.png'.format(
                desi_spectro_redux, self.night, exp_zfill)
            plt.savefig(ofn)

            # Try the options:
            url= ["""<img src="%s">"""%ofn,
                 ofn, 
                 "spec.png"][1]

            p = Figure(x_range=(0,200), y_range=(0,200))
            
            p.image_url( url= [ofn],
             x=100, y=100, w=180, h=100, anchor="center")
            p.plot_height=p.plot_width//2

            p.xaxis.major_tick_line_color = None  
            p.xaxis.minor_tick_line_color = None  
            p.yaxis.major_tick_line_color = None  
            p.yaxis.minor_tick_line_color = None 
            p.xaxis.major_label_text_font_size = '0pt'  # preferred method for removing tick labels
            p.yaxis.major_label_text_font_size = '0pt'
            p.xgrid.grid_line_color = None
            p.ygrid.grid_line_color = None
        #     f0.write("""<img src="%s">"""%ofn)

        # f0.write( "Execution time: "+ str( time.time()-t0 ))

        return file_html(p, CDN, "png")

