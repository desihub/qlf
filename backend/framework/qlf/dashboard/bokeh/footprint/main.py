import astropy
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
import os

from dashboard.models import Exposure


class Footprint():
    def footprint(self, coords, visibles):

        x = coords.ra*u.hour
        y = coords.dec*u.deg

        vx = visibles.ra*u.hour
        vy = visibles.dec*u.deg

        plot = figure(
            tools='box_zoom,pan,wheel_zoom,reset,lasso_select,crosshair',
            active_drag="box_zoom",
            height=450,
            sizing_mode='scale_width'
        )

        plot.circle(x, y, fill_color='black', alpha=0.1)

        plot.circle(vx, vy, fill_color='red', size=5, alpha=0.7)

        plot.xaxis.axis_label = "RA (hour)"
        plot.yaxis.axis_label = "DEC (deg)"

        return plot

    def render(self, exposures_radec):
        qlf_root = os.environ.get('QLF_ROOT', '/app')
        pointings_file = os.path.join(
            qlf_root, 'framework/qlf/dashboard/bokeh/footprint/noconstraints.dat')

        # you need to edit the original file to comment the header and join hourangle
        pointings = Table.read(pointings_file, format='ascii.commented_header')
        coords = SkyCoord(ra=pointings['RA']*u.hour,
                          dec=pointings['DEC']*u.deg, frame='icrs')
        if not exposures_radec['ra']:
            empty = SkyCoord(ra=[]*u.hour, dec=[]*u.deg, frame='icrs')
            return file_html(self.footprint(coords, empty), CDN, "DESI Footprint")
        visibles = SkyCoord(ra=exposures_radec['ra']*u.hour,
                            dec=exposures_radec['dec']*u.deg, frame='icrs')

        return file_html(self.footprint(coords, visibles), CDN, "DESI Footprint")
