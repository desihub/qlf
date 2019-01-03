import os
import logging
import requests
from furl import furl
from bokeh.plotting import Figure
from dashboard.models import Process, Job
from qlf_models import QLFModels
import sys

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

logger = logging.getLogger(__name__)


def get_merged_qa_scalar_metrics(process_id, cam):
    """
    Returns cam scalar metrics
    """

    return QLFModels().get_output(process_id, cam)


def init_xy_plot(hover, yscale):
    """
    Defaults for xy plots
    """
    plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset,tap"],active_drag="box_zoom",
                  y_axis_type=yscale, plot_width=601, plot_height=400)
    # plot.add_tools(hover)

    return plot


def get_palette(name_of_mpl_palette):
    """ Transforms a matplotlib palettes into a bokeh 
    palettes
    """
    import numpy as np
    from matplotlib.colors import rgb2hex
    import matplotlib.cm as cm
    # choose any matplotlib colormap here
    colormap = cm.get_cmap(name_of_mpl_palette)
    bokehpalette = [rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    return bokehpalette


if __name__ == '__main__':
    logger.info('Standalone execution...')
