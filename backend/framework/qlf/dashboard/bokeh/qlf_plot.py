import os
import logging
import pandas as pd
import requests
from furl import furl
from bokeh.plotting import Figure
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter


def sort_obj(gen_info):
    """ Hover info of objects type in fibers plots.
    """
    obj_type=['']*500
    for key in ['LRG', 'ELG', 'QSO', 'STAR','SKY']:
        if gen_info.get(key+'_FIBERID', None):
            for i in gen_info[key+'_FIBERID']:
                obj_type[i]=key
        else:
            pass
    return obj_type
                


def info_table(metricname, comments, keyname, delta, curexp='xxx', refexp='xxx'):
    """ Create tables in format
    delta = current val - refval
    """
    style = """    <style>        table {
            font-family: arial, sans-serif;
            font-size: 16px;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
            }
        tr:nth-child(even) {
        background-color: #dcdcdc;
                text-align:center;
        }
        tr:{text-align:center;}        </style>        """

    header= """
        <div  style="text-align:center;padding-left:20px;padding-top:10px;">
        <table>
        <tr>
        <th> Comments</th>  <th>keyname</th> <th>Current Exposure</th> <th>Reference Exposure</th>  <th>Delta</th>
        </tr>"""
    end="""</table> </div> """
    title="""<h2 style="text-align:center;">  {} </h2>""".format(metricname)
    
    tblines=""

    nlines=1
    for i in range(nlines):
        tblines=tblines+"""<tr>
                <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>""".format(comments,keyname,curexp,refexp,delta)
        

    return style + title + header + tblines + end



def alert_table(nrg,wrg):
    """ Create metric tables
    """
    style = """    <style>        table {
            font-family: arial, sans-serif;
            font-size: 16px;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
            }
        tr:nth-child(even) {
        background-color: #dcdcdc;
                text-align:center;
        }
        tr:{text-align:center;}        </style>        """

    header= """
        <div  style="text-align:center;padding-left:20px;padding-top:10px;">
        <table>
        <tr>
        <th> Alert </th>  <th>Minimum value</th> <th>Maximum value</th>
        </tr>"""

    end="""</table> </div> """

    
    nlines=1
    tblines="""<tr>
                <td>{}</td> <td>{}</td> <td>{}</td> 
                </tr>""".format('Normal',nrg[0],nrg[1])
    tblines= tblines+"""<tr>
                <td>{}</td> <td>{}</td> <td>{}</td> 
                </tr>""".format('Warning', wrg[0], wrg[1])        

    return style  + header + tblines + end


def metric_table(metricname, comments, keyname,  curexp='xxx', refexp='xxx', objtype=['XXELG', 'XXSTAR']):
    """ Create metric tables
    """
    
    style = """    <style>        table {
            font-family: arial, sans-serif;
            font-size: 16px;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
            }
        tr:nth-child(even) {
        background-color: #dcdcdc;
                text-align:center;
        }
        tr:{text-align:center;}
        </style>"""

    header= """
        <div  style="text-align:center;padding-left:20px;padding-top:10px;">
        <table>
              <col width="200">
              <col width="100">
              <col width="90">
              <col width="90">
        <tr>
        <th> Comments</th>  <th>keyname</th> <th>Current Exposure</th> <th>Reference Exposure</th>
        </tr>"""

    end="""</table> </div> """

    title="""<h2 align=center style="text-align:center;">  {} </h2>""".format(keyname)
    
    
    key_tb=[]
    curtb =(['???'])*len(curexp)

    if keyname in ['snr', 'integ']:
        # per_TGT
        for i in list(range(len(curexp))):
            key_tb.append(metricname +'  ( %s)'%objtype[i])
            try: curtb[i] = '{:4.3f}'.format(curexp[i])
            except: curtb[i] = '???'
        
    elif keyname in [ 'countpix','getbias','getrms']:
        #per AMP
        for i in list(range(len(curexp))):
            key_tb.append(metricname + ' (AMP %d)'%(i+1))
            try: curtb[i] = '{:4.3f}'.format(curexp[i])
            except: curtb[i] = '???'#curexp[i]
        
    elif keyname in ['xwsigma']:
        # per axis x or w
        for i in list(range(len(curexp))):
            key_tb.append(metricname + [' (x)',' (w)'][i])
            try: curtb[i] = '{:4.3f}'.format(curexp[i])
            except: curtb[i] = '???'#curexp[i]
                
    else:
        key_tb = ['xwsigma' if  'igma' in  metricname else metricname][0]
        try: curtb = curexp#'%3.2f'%(curexp)
        except: curtb='???'
    
    
    if isinstance(curexp, list):
        nrows=len(curexp)
        tblines=""
        for i in list(range(len(curexp))):
            if i ==0:
                tblines=tblines+\
                """<tr>
                <td rowspan="{}">{}</td> <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>
                """.format(nrows, comments, key_tb[i], curtb[i], refexp)

            else:
                tblines=tblines+\
                """<tr>
                <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>
                """.format( key_tb[i], curtb[i], refexp)
            
    else:
        tblines = """<tr>
                <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>""".format(comments, key_tb, curtb, refexp)
        

    return style + title + header + tblines + end



def mtable(qa, data, comments, objtype=['XXELG','XXSTAR']):
    import numpy as np
    # DEFINE qa_step
    # qa_metrics
    #     style, title, header, end='','','',''

    #comments='xxasdas '*4
    
    qa_metrics={}
    qa_metrics['countpix']= 'LITFRAC_AMP'
    qa_metrics['getbias']= 'BIAS_AMP'
    qa_metrics['getrms']= 'NOISE_AMP'
    qa_metrics['xwsigma']= 'XWSIGMA'
    qa_metrics['countbins']= 'NGOODFIB'
    qa_metrics['skycont']= 'SKYCONT'
    qa_metrics['skypeak']= 'PEAKCOUNT'
    qa_metrics['integ']= 'DELTAMAG_TGT'
    qa_metrics['skyresid']= 'MED_RESID'
    qa_metrics['snr']= 'FIDSNR_TGT'

    qa_step={
        'countpix': 'CHECK_CCDs',
        'getbias': 'CHECK_CCDs',
        'getrms': 'CHECK_CCDs',
        'xwsigma': 'CHECK_FIBERS',
        'countbins': 'CHECK_FIBERS',
        'skycont': 'CHECK_SPECTRA',
        'skypeak': 'CHECK_SPECTRA',
        'integ': 'CHECK_SPECTRA',
        'skyresid': 'CHECK_SPECTRA',
        'snr': 'CHECK_SPECTRA'}
    
    met=data['TASKS'][qa_step[qa]]['METRICS']
    par=data['TASKS'][qa_step[qa]]['PARAMS']
    key=qa_metrics[qa]
 
    style = """    <style>        table {
            font-family: arial, sans-serif;
            font-size: 16px;
            border-collapse: collapse;
            width: 100%;
            }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
            }
        tr:nth-child(even) {
        background-color: #dcdcdc;
                text-align:center;
        }
        tr:{text-align:center;}
        </style>"""

    header= """
        <div  style="text-align:center;padding-left:20px;padding-top:10px;">
        <table>
              <col width="200">
              <col width="120">
              <col width="90">
              <col width="90">
        <tr>
        <th> Comments</th>  <th>keyname</th> <th>Current Exposure</th> <th>Reference Exposure</th>
        </tr>"""

    end="""</table> </div> """

    title="""<h2 align=center style="text-align:center;">  {} </h2>""".format(qa)


    if qa=='countpix':
        ref=['N/A']*4
        nrows=4
    else:
        ref=par[key+'_REF']
        if isinstance(ref,list):
            nrows=len(ref)
        else:
            nrows=1
    
    try:
        curexp=met[key]
    except Exception as err:
        if nrows==1: 
            curexp= 'key N/A'
        else:
            curexp = ['key N/A']*nrows

    
    if nrows > 1:
        cur_tb, ref_tb=[],[]
        for i in list(range(nrows)):
            x = curexp[i]
            ref_tb.append(ref[i])
            
            if isinstance(x, float) and x > -999:
                xstr='%4.3f'%(x)
            elif isinstance(x, float) and (x <=-999 or x == np.nan):
                xstr='NaN'
            elif isinstance(x, int):
                xstr='%d'%x
            else:
                xstr='???'
                
            cur_tb.append(xstr)
    elif nrows==1:
        if isinstance(curexp, float):
            cur_tb='%4.3f'%curexp
            ref_tb='%2.1f'%ref
        elif isinstance(curexp, int):
            cur_tb='%d'%curexp
            ref_tb=ref
        else:
            cur_tb=curexp
            ref_tb=ref
            

    if qa in ['snr', 'integ']:
        # per_TGT
        if objtype is not None:
            objtype_tb = ['STAR' if i=='STD' else i for i in objtype]
            key_tb= [qa_metrics[qa] + ' ( %s)'%objtype_tb[i] for i in list(range(nrows))]
        else:
            key_tb= [qa_metrics[qa]] *nrows

       
    elif qa in [ 'countpix','getbias','getrms']:
        #per AMP
        key_tb= [qa_metrics[qa] + ' (AMP %d)'%(i+1) for i in list(range(nrows))]
        
    elif qa in ['xwsigma']:
        # per axis x or w
        key_tb = [ qa_metrics[qa] + [' (x)',' (w)'][i] for i in list(range(nrows))]
    else:
        key_tb=key
        #cur_tb=curexp
        #ref_tb=ref
                
    
    tblines=""
    for i in  list(range(nrows)):
        if nrows==1:
            tblines=tblines+\
                """<tr>
                <td rowspan="{}">{}</td> <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>
                """.format(nrows, comments, key, cur_tb, ref_tb)
        elif i ==0:
            tblines=tblines+\
                """<tr>
                <td rowspan="{}">{}</td> <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>
                """.format(nrows, comments, key_tb[i], cur_tb[i], ref_tb[i])
        else:
            tblines=tblines+\
                """<tr>
                <td>{}</td> <td>{}</td> <td>{}</td>
                </tr>
                """.format( key_tb[i], cur_tb[i], ref_tb[i])

    print(cur_tb, ref_tb)
    return style + header + tblines + end



def range_table(names=[], vals=[], nkey='Normal Range', wkey='Warning Range', nrng=[0,0],  wrng=[0,0], nlines=None, align='center'):
    ''' Usage Example:
            table_txt = html_table( nrng=nrg, wrng=wrg  )
            tbinfo = Div(text=table_txt, width=600, height=300)
    '''
    lines =""" """
    tblines=""" """
    nlines= len(names)
    if(nlines != len(vals)):
        print('error in table')
        return """error in table"""

    style = """
    <style>
        table {
            font-family: arial, sans-serif;
            font-size: 16px;
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

    header= """
    <div  style="text-align:center;padding-left:20px;padding-top:10px;">
    <table>
    <tr>
        <th>Alert</th>     <th>Minimum Value</th>        <th>Maximum Value</th>
    </tr>"""


    for i1,i2 in [[nkey, nrng], [wkey, wrng]]:
        lines = lines+"""
        <tr>
            <td>{}</td>
            <td> {:.2f}</td>  <td>{:.2f}</td>
        </tr>""".format( i1, i2[0], i2[1] )
    
    end="""</table> </div> """

    return style+header+ tblines+lines+end



def html_table(names=[], vals=[], nkey='Normal Range', wkey='Warning Range', nrng=[0,0],  wrng=[0,0], nlines=None, align='center'):
    lines =""" """
    tblines=""" """
    nlines= len(names)
    if(nlines != len(vals)):
        print('error in table')

    if(nlines==0):
        tblines=""
    else:
        for i in range(nlines):
            if isinstance(vals[i], list):
                tblines=tblines+"""<tr>
                <td>{}</td>
                <td> {}</td>
                </tr>""".format(names[i], vals[i])#, vals[i][0] )

            elif( names[i]=='NGOODFIB'):
                tblines=tblines+"""<tr>
                <td>{}</td>
                <td> {:d}</td>
                </tr>""".format(names[i], vals[i])
            elif(isinstance(vals[i],str)):
                tblines=tblines+"""<tr>
                <td>{}</td>
                <td> {}</td>
                </tr>""".format(names[i], vals[i])
            elif(isinstance(vals[i],float)):
                tblines=tblines+"""<tr>
                <td>{}</td>
                <td> {:.3f}</td>
                </tr>""".format(names[i], vals[i])

            else:
                tblines=tblines+"""<tr>
                <td>{}</td>
                <td> {:.3f}</td>
                </tr>""".format(names[i], vals[i])


    style = """
    <style>
        table {
            font-family: arial, sans-serif;
            font-size: 16px;
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

    header= """
    <div>
    <table>
    <tr>
        <th>Parameter</th>        <th>Value</th>
    </tr>"""


    for i1,i2 in [(nkey, nrng), (wkey, wrng)]:
        lines = lines+"""
        <tr>
            <td>{}</td>
            <td> [{:.2f},  {:.2f}]</td>
        </tr>""".format(i1, i2[0], i2[1] )
    
    end="""</table> </div> """

    return style+header+ tblines+lines+end



def plot_hist(hover,yrange, yscale="auto", pw=600, ph=400):
    """
    Defaults for histograms
    """
    if yscale not in ["log","auto"]:
        logger.warn('Wrong yscale')
    if yrange==None:
        plot = Figure(tools=[hover,"pan,wheel_zoom,box_zoom,reset, crosshair, tap"] 
            , plot_width=pw, plot_height=ph, background_fill_color="white"
            , x_axis_type="auto", y_axis_type=yscale)

    else:    
        plot = Figure(tools=[hover,"pan,wheel_zoom,box_zoom,reset, crosshair, tap"] 
            , plot_width=pw, plot_height=ph, background_fill_color="white"
            , x_axis_type="auto", y_axis_type=yscale
            , y_range =yrange)

    #plot.add_tools(hover)
    
    return plot


def set_amp(z_value):
    ''' Setup for AMP plots
    '''
    import numpy as np
    dz=z_value
    dzmax, dzmin = max(dz), min(dz) 

    if np.log10(dzmax) > 4 or np.log10(dzmin) <-3:
        ztext = ['{:4.3e}'.format(i) for i in dz]
        cbarformat = "%2.1e"
    elif np.log10(dzmin)>0:
        ztext = ['{:5.4f}'.format(i) for i in dz]
        cbarformat = "%4.2f"
    else:
        ztext = ['{:6.5f}'.format(i) for i in dz]
        cbarformat = "%5.4f"

    return  ztext, cbarformat


def plot_amp(dz, mapper, name=""):
    ''' Initializing AMP plot
    '''
    ztext, cbarformat = set_amp(dz)
    dx = [0,1,0,1]
    dy = [1,1,0,0]

    cmap_tooltip = """
        <div>
            <div>
                <span style="font-size: 12px; font-weight: bold; color: #303030;">counts: </span>
                <span style="font-size: 13px; color: #515151">@z</span>
            </div>
            <div>
                <span style="font-size: 12px; font-weight: bold; color: #303030;">AMP: </span>
                <span style="font-size: 13px; color: #515151;">@amp</span>
            </div>
        </div>
    """.replace("counts:", name+":")
    hover = HoverTool(tooltips=cmap_tooltip)

    p = Figure(title=name, tools=[hover],
           x_range= list([-0.5,1.5]),           # length = 18
           y_range= list([-0.5,1.5]), 
           plot_width=450, plot_height=400)

    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.axis.clear
    p.axis.minor_tick_line_color=None
    
    p.xaxis.major_label_text_font_size = '0pt'  
    p.yaxis.major_label_text_font_size = '0pt'  
    p.xaxis.major_tick_line_color = None  
    p.xaxis.minor_tick_line_color = None  
    p.yaxis.major_tick_line_color = None  
    p.yaxis.minor_tick_line_color = None  

    source = ColumnDataSource(
        data=dict(
            x = dx,
            y = dy,
            z = dz,
            y_offset1 = [i+0.15 for i in dy],
            y_offset2 = [i-0.05 for i in dy],
            amp = ['AMP %s'%i for i in range(1,5) ] ,
            ztext = ztext
            )
        )

    text_props = {
        "source": source,
        "angle": 0,
        "color": "black",
        "text_color":"black",
        "text_align": "center",
        "text_baseline": "middle"}


    p.rect("x", "y", .98, .98, 0, source=source,
           fill_color={'field': 'z', 'transform': mapper}, fill_alpha=0.9)

    p.text(x="x", y="y_offset2", text="ztext",
           text_font_style="bold", text_font_size="20pt", **text_props)
    p.text(x="x", y="y_offset1", text="amp",
            text_font_size="18pt", **text_props)
    

    return p



if __name__=='__main__':
    logger.info('Standalone execution')
