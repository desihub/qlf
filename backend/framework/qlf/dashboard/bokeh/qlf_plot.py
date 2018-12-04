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

def alert_table(nrg, wrg):
    """ Create metric tables
    """
    style = """    <style>        table {
            font-family: arial, sans-serif;
            font-size: 1vw;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            }
        tr:nth-child(even) {
        background-color: #dcdcdc;
                text-align:center;
        }
        tr:{text-align:center;}        </style>        """

    header = """
        <div  style="text-align:center;padding-left:20px;padding-top:10px;">
        <table>
        <tr>
        <th> Alert </th>  <th>Minimum value</th> <th>Maximum value</th>
        </tr>"""

    end = """</table> </div> """

    nlines = 1
    tblines = """<tr>
                <td>{}</td> <td>{}</td> <td>{}</td> 
                </tr>""".format('Normal', nrg[0], nrg[1])
    tblines = tblines+"""<tr>
                <td>{}</td> <td>{}</td> <td>{}</td> 
                </tr>""".format('Warning', wrg[0], wrg[1])

    return style + header + tblines + end


def metric_table(metricname, keyname,  curexp='xxx', refexp='xxx', objtype=['XXELG', 'XXSTAR']):
    """ Create metric tables
    """

    style = """    <style>        table {
            font-family: arial, sans-serif;
            font-size: 1vw;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            }
        tr:nth-child(even) {
        background-color: #dcdcdc;
                text-align:center;
        }
        tr:{text-align:center;}
        </style>"""

    header = """
        <div  style="text-align:center;padding-left:20px;padding-top:10px;">
        <table>
              <col width="200">
              <col width="100">
              <col width="90">
              <col width="90">
        <tr>
          <th>keyname</th> <th>Current Exposure</th> <th>Reference Exposure</th>
        </tr>"""

    end = """</table> </div> """

    title = """<h2 align=center style="text-align:center;">  {} </h2>""".format(
        keyname)

    key_tb = []
    curtb = (['???'])*len(curexp)

    if keyname in ['snr', 'integ']:
        # per_TGT
        for i in list(range(len(curexp))):
            key_tb.append(metricname + '  ( %s)' % objtype[i])
            try:
                curtb[i] = '{:4.3f}'.format(curexp[i])
            except:
                curtb[i] = '???'

    elif keyname in ['countpix', 'getbias', 'getrms']:
        # per AMP
        for i in list(range(len(curexp))):
            key_tb.append(metricname + ' (AMP %d)' % (i+1))
            try:
                curtb[i] = '{:4.3f}'.format(curexp[i])
            except:
                curtb[i] = '???'  # curexp[i]

    elif keyname in ['xwsigma']:
        # per axis x or w
        for i in list(range(len(curexp))):
            key_tb.append(metricname + [' (x)', ' (w)'][i])
            try:
                curtb[i] = '{:4.3f}'.format(curexp[i])
            except:
                curtb[i] = '???'  # curexp[i]

    else:
        key_tb = ['xwsigma' if 'igma' in metricname else metricname][0]
        try:
            curtb = curexp  # '%3.2f'%(curexp)
        except:
            curtb = '???'

    if isinstance(curexp, list):
        nrows = len(curexp)
        tblines = ""
        for i in list(range(len(curexp))):
            if i == 0:
                tblines = tblines +\
                    """<tr>
                    <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>
                """.format(nrows, key_tb[i], curtb[i], refexp)

            else:
                tblines = tblines +\
                    """<tr>
                <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>
                """.format(key_tb[i], curtb[i], refexp)

    else:
        tblines = """<tr>
                  <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>""".format(key_tb, curtb, refexp)

    return style + title + header + tblines + end


def mtable(qa, data, objtype=['OTYPE ?', 'OTYPE ?']):
    qa_metrics = {}
    qa_metrics['countpix'] = 'LITFRAC_AMP'
    qa_metrics['getbias'] = 'BIAS_AMP'
    qa_metrics['getrms'] = 'NOISE_AMP'
    qa_metrics['xwsigma'] = 'XWSIGMA'
    qa_metrics['countbins'] = 'NGOODFIB'
    qa_metrics['skycont'] = 'SKYCONT'
    qa_metrics['skypeak'] = 'PEAKCOUNT'
    qa_metrics['integ'] = 'DELTAMAG_TGT'
    qa_metrics['skyresid'] = 'MED_RESID'
    qa_metrics['snr'] = 'FIDSNR_TGT'
    qa_metrics['fiberflat']= 'CHECKFLAT'
    qa_metrics['arc']= 'CHECKARC'
    qa_metrics['xyshifts']= 'XYSHIFTS'
    qa_metrics['skyR']= 'SKYRBAND'

    qa_step = {
        'countpix': 'CHECK_CCDs',
        'getbias': 'CHECK_CCDs',
        'getrms': 'CHECK_CCDs',
        'xwsigma': 'CHECK_FIBERS',
        'countbins': 'CHECK_FIBERS',
        'skycont': 'CHECK_SPECTRA',
        'skypeak': 'CHECK_SPECTRA',
        'integ': 'CHECK_SPECTRA',
        'skyresid': 'CHECK_SPECTRA',
        'snr': 'CHECK_SPECTRA',
        'fiberflat': "CHECK_FIBERFLAT",
        'arc': "CHECK_ARC",
        'xyshifts': "CHECK_FIBERS",
        'skyR': "CHECK_SPECTRA",}

    met = data['TASKS'][qa_step[qa]]['METRICS']
    par = data['TASKS'][qa_step[qa]]['PARAMS']
    key = qa_metrics[qa]

    style = """    <style>        table {
            font-family: arial, sans-serif;
            font-size: 1.3vw;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            }
        tr:nth-child(even) {
        background-color: #dcdcdc;
                text-align:center;
        }
        tr:{text-align:center;}
        </style>"""

    header = """
        <div  style="text-align:center;padding-left:20px;padding-top:10px;">
        <table>
              <col width="120">
              <col width="90">
              <col width="90">
        </tr>
        <tr>
            <th>keyname</th> <th>Current Exposure</th> <th>Reference Exposure</th>
        </tr>"""

    end = """</table> </div> """

    title = """<h2 align=center style="text-align:center;">  {} </h2>""".format(
        qa)

    if qa == 'NAcountpix':
        ref = ['N/A']*4
        nrows = 4
    else:
        if data['FLAVOR'].upper() == 'SCIENCE':
            program = data['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''

        try:
            ref=par[key+program_prefix+'_REF']
        except:
            if qa =='xyshifts':
                ref=[np.NaN]*2

        if qa =='snr':
            nrows=len(met['OBJLIST'])
        elif qa == 'fiberflat': 
            # Solving for wrong lenght in ref list
            nrows=1
            ref=ref[0]
        elif isinstance(ref,list):
            nrows=len(ref)
        else:
            nrows = 1


    try:
        curexp = met[key]
    except Exception as err:
        if nrows == 1:
            curexp = 'key N/A'
        else:
            curexp = ['key N/A']*nrows

    if nrows > 1:
        cur_tb, ref_tb = [], []
        for i, x in enumerate(curexp):
            if qa=='arc':
                ref_tb.append('%d'%ref[i])
            elif (qa=='snr') & (nrows != len(ref)):
                try: ref_tb.append('%.2f'%ref[i])
                except: ref_tb.append('')
            else:
                ref_tb.append('%.2f'%ref[i])

            if isinstance(x, float) and x > -999:
                xstr = '%.2f' % (x)
            elif isinstance(x, float) and (x <= -999 or x == np.nan):
                xstr = 'NaN'
            elif isinstance(x, int):
                xstr = '%d' % x
            else:
                xstr = '???'

            cur_tb.append(xstr)
    elif nrows == 1:
        if qa=='fiberflat':
            # Solving for wrong length in list
            try: curexp=curexp[0]
            except: pass
        if isinstance(curexp, float):
            cur_tb = '%.2f' % curexp
            ref_tb = '%.2f' % ref[0]
        elif isinstance(curexp, int):
            cur_tb = '%d' % curexp
            try:
                ref_tb = '%d'%ref[0]
            except:
                ref_tb=ref
        else:
            cur_tb = curexp
            ref_tb = ref

    if qa in ['snr', 'integ']:
        # per_TGT
        if objtype is not None:
            objtype_tb = ['STAR' if i == 'STD' else i for i in objtype]
            key_tb = [qa_metrics[qa]+" (%s)"%x for x in objtype_tb ]# * nrows
            # key_tb = [qa_metrics[qa] + ' ( %s)' % objtype_tb[i]
            #   for i in list(range(nrows))]
        else:
            key_tb = [qa_metrics[qa]] * nrows

    elif qa in ['countpix', 'getbias', 'getrms']:
        # per AMP
        key_tb = [qa_metrics[qa] 
                  for i in list(range(nrows))]

    elif qa in ['xwsigma']:
        # per axis x or w
        key_tb = [qa_metrics[qa] + [' (x)', ' (w)'][i]
                  for i in list(range(nrows))]

    elif qa in ['arc']:
        key_tb = [qa_metrics[qa]+ " ( P%d)"%i for i in range(3)]
    elif qa in ['xyshifts']:
        key_tb = [qa_metrics[qa]+ " ( %s)"%i for i in ['X','Y'] ]

    else:
        key_tb = key
        # cur_tb=curexp
        # ref_tb=ref

    tblines = ""

    if qa == 'integ':
        for i, x in enumerate(curexp):
            if nrows == 1:
                tblines = tblines +\
                    """<tr>
                    <td>{}</td> <td>{}</td> <td>{}</td>
                    </tr>
                    """.format(key, cur_tb, ref_tb)
                    #                <td rowspan="{}">{}</td> <td>{}</td> <td>{}</td>
            elif i == 0:
                tblines = tblines +\
                    """<tr>
                    <td>{}</td> <td>{}</td> <td>{}</td>
                    </tr>
                    """.format(key_tb[i], cur_tb[i], ref_tb[i])
            else:
                tblines = tblines +\
                    """<tr>
                    <td>{}</td> <td>{}</td> <td>{}</td>
                    </tr>
                    """.format(key_tb[i], cur_tb[i], ref_tb[i])
    else:
        for i in list(range(nrows)):
            if nrows == 1:
                tblines = tblines +\
                    """<tr>
                    <td>{}</td> <td>{}</td> <td>{}</td>
                    </tr>
                    """.format(key, cur_tb, ref_tb)
                    #                <td rowspan="{}">{}</td> <td>{}</td> <td>{}</td>
            elif i == 0:
                tblines = tblines +\
                    """<tr>
                    <td>{}</td> <td>{}</td> <td>{}</td>
                    </tr>
                    """.format(key_tb[i], cur_tb[i], ref_tb[i])
            else:
                tblines = tblines +\
                    """<tr>
                    <td>{}</td> <td>{}</td> <td>{}</td>
                    </tr>
                    """.format(key_tb[i], cur_tb[i], ref_tb[i])

    return style + header + tblines + end



def range_table(names=[], vals=[], nkey='Normal Range', wkey='Warning Range', nrng=[0, 0],  wrng=[0, 0], nlines=None, align='center'):
    ''' Usage Example:
            table_txt = html_table( nrng=nrg, wrng=wrg  )
            tbinfo = Div(text=table_txt, width=600, height=300)
    '''
    lines = """ """
    tblines = """ """
    nlines = len(names)
    if(nlines != len(vals)):
        return """error in table"""

    style = """
    <style>
        table {
            font-family: arial, sans-serif;
            font-size: 1vw;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
            }
        tr:nth-child(even) {
        background-color: #dddddd;
                text-align:center;
        }
        tr:{text-align:center;}
        </style>
        """

    header = """
    <div  style="text-align:center;padding-left:20px;padding-top:10px;">


    <table>
    <tr>
        <th>Alert</th>     <th>Minimum Value</th>        <th>Maximum Value</th>
    </tr>"""

    for i1, i2 in [[nkey, nrng], [wkey, wrng]]:
        lines = lines+"""
        <tr>
            <td>{}</td>
            <td> {:.2f}</td>  <td>{:.2f}</td>
        </tr>""".format(i1, i2[0], i2[1])

    end = """</table> </div> """

    return style+header + tblines+lines+end


def html_table(names=[], vals=[], nkey='Normal Range', wkey='Warning Range', nrng=[0, 0],  wrng=[0, 0], nlines=None, align='center'):
    lines = """ """
    tblines = """ """
    nlines = len(names)
    if(nlines != len(vals)):
        print('error in table')

    if(nlines == 0):
        tblines = ""
    else:
        for i in range(nlines):
            if isinstance(vals[i], list):
                tblines = tblines+"""<tr>
                <td>{}</td>
                <td> {}</td>
                </tr>""".format(names[i], vals[i])  # , vals[i][0] )

            elif(names[i] == 'NGOODFIB'):
                tblines = tblines+"""<tr>
                <td>{}</td>
                <td> {:d}</td>
                </tr>""".format(names[i], vals[i])
            elif(isinstance(vals[i], str)):
                tblines = tblines+"""<tr>
                <td>{}</td>
                <td> {}</td>
                </tr>""".format(names[i], vals[i])
            elif(isinstance(vals[i], float)):
                tblines = tblines+"""<tr>
                <td>{}</td>
                <td> {:.3f}</td>
                </tr>""".format(names[i], vals[i])

            else:
                tblines = tblines+"""<tr>
                <td>{}</td>
                <td> {:.3f}</td>
                </tr>""".format(names[i], vals[i])

    style = """
    <style>
        table {
            font-family: arial, sans-serif;
            font-size: 1vw;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            }
        tr:nth-child(even) {
        background-color: #dddddd;
                text-align:center;
        }
        tr:{text-align:center;}
        </style>
        """

    header = """
    <div>
    <table>
    <tr>
        <th>Parameter</th>        <th>Value</th>
    </tr>"""

    for i1, i2 in [(nkey, nrng), (wkey, wrng)]:
        lines = lines+"""
        <tr>
            <td>{}</td>
            <td> [{:.2f},  {:.2f}]</td>
        </tr>""".format(i1, i2[0], i2[1])

    end = """</table> </div> """

    return style+header + tblines+lines+end


def plot_hist(hover, yrange, yscale="auto", pw=600, ph=400):
    """
    Defaults for histograms
    """
    if yscale not in ["log", "auto"]:
        logger.warn('Wrong yscale')
    if yrange == None:
        plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset, crosshair, tap"], plot_width=pw, active_drag="box_zoom",
                      plot_height=ph, background_fill_color="white", x_axis_type="auto", y_axis_type=yscale)

    else:
        plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset, crosshair, tap"], plot_width=pw, active_drag="box_zoom",
                      plot_height=ph, background_fill_color="white", x_axis_type="auto", y_axis_type=yscale, y_range=yrange)

    # plot.add_tools(hover)

    return plot


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


def plot_amp(dz, refexp, mapper, name="", font_size="1.2vw"):
    ''' Initializing AMP plot
    '''
    ztext, cbarformat = set_amp(dz)
    dx = [0, 1, 0, 1]
    dy = [1, 1, 0, 0]

    cmap_tooltip = """
        <div>

            <div>
                <span style="font-size: 1vw; font-weight: bold; color: #303030;">AMP: </span>
                <span style="font-size: 1vw; color: #515151;">@amp_number</span>
            </div>
            <div>
                <span style="font-size: 1vw; font-weight: bold; color: #303030;">counts: </span>
                <span style="font-size: 1vw; color: #515151">@ztext</span>
            </div>
            <div>
                <span style="font-size: 1vw; font-weight: bold; color: #303030;">Reference: </span>
                <span style="font-size: 1vw; color: #515151;">@ref</span>
            </div>
         </div>
    """.replace("counts:", name.replace("_AMP","")+":")
    hover = HoverTool(tooltips=cmap_tooltip)

    p = Figure(title=name, tools=[hover],
               x_range=list([-0.5, 1.5]),
               y_range=list([-0.5, 1.5]),
               plot_width=450, plot_height=400)


    p.xaxis.axis_label_text_font_size = font_size
    p.legend.label_text_font_size = font_size
    p.title.text_font_size = font_size

    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.axis.clear
    p.axis.minor_tick_line_color = None

    p.axis.major_label_text_font_size = '0pt'
    p.yaxis.major_label_text_font_size = '0pt'
    #p.xaxis.axis_label_text_font_size = "0pt"
    p.xaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.yaxis.visible = False
    p.xaxis.visible = True



    zvalid=[x if x>-999 else np.nan for x in dz]
    source = ColumnDataSource(
        data=dict(
            x = dx,
            y = dy,
            z = dz,
            zvalid = zvalid,
            ref=["{:.2f}".format(x) for x in refexp],
            zdiff = np.array(zvalid) -np.array(refexp),
            y_offset1 = [i+0.15 for i in dy],
            y_offset2 = [i-0.10 for i in dy],
            amp = ['AMP %s'%i for i in range(1,5) ] ,
            amp_number = ['%s'%i for i in range(1,5) ] ,
            ztext = ztext,
            )
        )

    text_props = {
        "source": source,
        "angle": 0,
        "color": "black",
        "text_color": "black",
        "text_align": "center",
        "text_baseline": "middle"}

    p.rect("x", "y", .98, .98, 0, source=source,
           fill_color={'field': 'zdiff', 'transform': mapper}, fill_alpha=0.9)

    p.text(x="x", y="y_offset1", text="amp",
            text_font_size="2vw", **text_props)
    p.text(x="x", y="y_offset2", text="ztext",
           text_font_style="bold", text_font_size="2.5vw", **text_props)
    

    return p


if __name__ == '__main__':
    logger.info('Standalone execution')
