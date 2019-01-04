from bokeh.plotting import Figure
from qlf_models import QLFModels

def get_merged_qa_scalar_metrics(process_id, cam):
    """
    Returns cam scalar metrics
    """

    return QLFModels().get_output(process_id, cam)

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
