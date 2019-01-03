import os
import logging
import pandas as pd
import requests
from furl import furl
from bokeh.plotting import Figure
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from scalar_metrics import LoadMetrics
import numpy as np


def sort_obj(gen_info):
    """ Hover info of objects type in fibers (wedge) plots.
            input: gen_info= mergedqa['GENERAL_INFO']
            returns: list(500)
    """
    obj_type = ['']*500
    for key in ['LRG', 'ELG', 'QSO', 'STAR', 'SKY']:
        if gen_info.get(key+'_FIBERID', None):
            for i in gen_info[key+'_FIBERID']:
                obj_type[i] = key
        else:
            pass
    return obj_type

def set_amp(z_value):
    ''' Setup for AMP plots
    '''
    import numpy as np
    dz=z_value

    # removing NaN in ranges
    dz_valid=[ x if x > -999 else np.nan for x in dz ]
    dzmax, dzmin = np.nanmax(dz_valid), np.nanmin(dz_valid) 

    if np.log10(dzmax) > 4 or np.log10(dzmin) <-3:
        ztext = ['{:4.2e}'.format(i) for i in dz_valid]
        cbarformat = "%2.1e"
    elif np.log10(dzmin)>0:
        ztext = ['{:5.2f}'.format(i) for i in dz_valid]
        cbarformat = "%4.2f"
    else:
        ztext = ['{:6.2f}'.format(i) for i in dz_valid]
        cbarformat = "%5.2f"

    return ztext, cbarformat

