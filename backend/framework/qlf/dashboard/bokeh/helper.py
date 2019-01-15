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


def sort_obj(gen_info):
    """ Hover info of objects type in fibers (wedge) plots.
            input: gen_info= mergedqa['GENERAL_INFO']
            returns: list(500)
    """
    obj_type = ['']*500
    for key in ['LRG', 'ELG', 'QSO', 'STAR', 'SKY']:
        if gen_info.get(key+'_FIBERID', None):
            print(key+'_FIBERID', len(gen_info[key+'_FIBERID']))
            for i in gen_info[key+'_FIBERID']:
                obj_type[i%500] = key
        else:
            pass
    return obj_type
