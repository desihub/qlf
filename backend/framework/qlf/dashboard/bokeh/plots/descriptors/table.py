from bokeh.models.widgets import Div
from bokeh.layouts import widgetbox
import numpy as np

class Table:
    def alert_table(self, nrg, wrg):
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

        table = style + header + tblines + end
        return widgetbox(Div(text=table))


    def mtable(self, qa, data, objtype=['OTYPE ?', 'OTYPE ?']):
        qa_metrics = {}
        qa_metrics['countpix'] = 'LITFRAC_AMP'
        qa_metrics['getbias'] = 'BIAS_AMP'
        qa_metrics['getrms'] = 'NOISE_AMP'
        qa_metrics['xwsigma'] = 'XWSIGMA'
        qa_metrics['countbins'] = 'NGOODFIB'
        qa_metrics['skycont'] = 'SKYCONT'
        qa_metrics['skypeak'] = 'PEAKCOUNT'
        qa_metrics['integ'] = 'DELTAMAG_TGT'
        qa_metrics['snr'] = 'FIDSNR_TGT'
        qa_metrics['fiberflat'] = 'CHECKFLAT'
        qa_metrics['arc'] = 'CHECKARC'
        qa_metrics['xyshifts'] = 'XYSHIFTS'
        qa_metrics['skyR'] = 'SKYRBAND'

        qa_step = {
            'countpix': 'CHECK_CCDs',
            'getbias': 'CHECK_CCDs',
            'getrms': 'CHECK_CCDs',
            'xwsigma': 'CHECK_CCDs',
            'countbins': 'CHECK_FIBERS',
            'skycont': 'CHECK_SPECTRA',
            'skypeak': 'CHECK_SPECTRA',
            'integ': 'CHECK_SPECTRA',
            'snr': 'CHECK_SPECTRA',
            'fiberflat': "CHECK_FIBERFLAT",
            'arc': "CHECK_ARC",
            'xyshifts': "CHECK_FIBERS",
            'skyR': "CHECK_SPECTRA", }

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
                ref = par[key+program_prefix+'_REF']
            except:
                if qa == 'xyshifts' or qa == 'xwsigma':
                    ref = [np.NaN]*2

            if qa == 'snr':
                nrows = len(met['OBJLIST'])
            elif qa == 'fiberflat':
                # Solving for wrong lenght in ref list
                nrows = 1
                ref = ref[0]
            elif ref and isinstance(ref, list):
                nrows = len(ref)
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
                if qa == 'arc':
                    ref_tb.append('%d' % ref[i])
                elif (qa == 'snr') & (nrows != len(ref)):
                    try:
                        ref_tb.append('%.2f' % ref[i])
                    except:
                        ref_tb.append('')
                else:
                    ref_tb.append('%.2f' % ref[i])

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
            if qa == 'fiberflat':
                # Solving for wrong length in list
                try:
                    curexp = curexp[0]
                except:
                    pass
            if isinstance(curexp, float):
                cur_tb = '%.2f' % curexp
                ref_tb = '%.2f' % ref[0]
            elif isinstance(curexp, int):
                cur_tb = '%d' % curexp
                try:
                    ref_tb = '%d' % ref[0]
                except:
                    ref_tb = ref
            else:
                cur_tb = curexp
                ref_tb = ref

        if qa in ['snr', 'integ']:
            # per_TGT
            if objtype is not None:
                objtype_tb = ['STAR' if i == 'STD' else i for i in objtype]
                key_tb = [qa_metrics[qa]+" (%s)" %
                        x for x in objtype_tb]  # * nrows
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
            key_tb = [qa_metrics[qa] + " ( P%d)" % i for i in range(3)]
        elif qa in ['xyshifts']:
            key_tb = [qa_metrics[qa] + " ( %s)" % i for i in ['X', 'Y']]

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

        table = style + header + tblines + end
        return widgetbox(Div(text=table))
