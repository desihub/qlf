from bokeh.layouts import column, gridplot, widgetbox

from bokeh.models import Span, Label

from bokeh.models import ColumnDataSource, Range1d, OpenURL
from bokeh.models import LinearColorMapper, ColorBar
from qlf_models import QLFModels
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import Div
from bokeh.resources import CDN
from bokeh.embed import file_html
import numpy as np
from dashboard.bokeh.helper import get_palette, sort_obj
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.patch.main import Patch
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.plot2d.main import Plot2d


class Xwsigma:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):

        cam = self.selected_arm+str(self.selected_spectrograph)

        mergedqa = QLFModels().get_output(self.selected_process_id, cam)

        gen_info = mergedqa['GENERAL_INFO']
        flavor= mergedqa['FLAVOR']

        if flavor=="science":
            ra = gen_info['RA']
            dec = gen_info['DEC']

        check_ccds = mergedqa['TASKS']['CHECK_CCDs']

        xwsigma = check_ccds['METRICS']['XWSIGMA']
        xw_amp = check_ccds['METRICS']['XWSIGMA_AMP']

        xw_fib = check_ccds['METRICS']['XWSIGMA_FIB']

        nrg = check_ccds['PARAMS']['XWSIGMA_NORMAL_RANGE']
        wrg = check_ccds['PARAMS']['XWSIGMA_WARN_RANGE']
        obj_type = sort_obj(gen_info)  # [""]*500

        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        xw_ref = check_ccds['PARAMS']['XWSIGMA'+program_prefix+'_REF']

        xsigma = xw_fib[0]
        wsigma = xw_fib[1]

        delta_rg = wrg[1] - wrg[0]
        hist_rg = (wrg[0] - 0.1*delta_rg, wrg[1]+0.1*delta_rg)

        my_palette = get_palette("RdYlBu_r")

        xfiber = np.arange(len(xsigma))
        wfiber = np.arange(len(wsigma))
        if mergedqa['FLAVOR'].upper() != 'SCIENCE':
            ra = np.full(500,np.nan)
            dec= np.full(500,np.nan)

        source = ColumnDataSource(data={
            'x1': ra,  
            'y1': dec, 
            'xsigma': xsigma,
            'wsigma': wsigma,
            'delta_xsigma': np.array(xsigma) - xw_ref[0],
            'delta_wsigma': np.array(wsigma) - xw_ref[1],
            'xref':[xw_ref[0]]*len(xsigma),
            'wref':[xw_ref[1]]*len(xsigma),            
            'xfiber': xfiber,
            'wfiber': wfiber,
            'OBJ_TYPE': obj_type,
            'left': np.arange(0, 500)-0.4,
            'right': np.arange(0, 500)+0.4,
            'bottom': [0]*500
            })

        xsigma_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">XSigma: </span>
                    <span style="font-size: 1vw; color: #515151">@xsigma</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Reference: </span>
                    <span style="font-size: 1vw; color: #515151">@xref</span>
                </div>

                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 1vw; color: #515151;">@OBJ_TYPE</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1vw; color: #515151;">@x1</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 1vw; color: #515151;">@y1</span>
                </div>

                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@xfiber</span>
                </div>

                </div>
            """

        wsigma_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">WSigma: </span>
                    <span style="font-size: 1vw; color: #515151">@wsigma</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Reference: </span>
                    <span style="font-size: 1vw; color: #515151">@wref</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 1vw; color: #515151;">@OBJ_TYPE</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1vw; color: #515151;">@x1</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 1vw; color: #515151;">@y1</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@wfiber</span>
                </div>

            </div>
            """

        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        # determining the position of selected cam fibers:
        obj_type = sort_obj(gen_info)
        # ---------------------------------

        if flavor=="science":
            

            # axes limit
            xmin, xmax = [min(ra[:]), max(ra[:])]
            ymin, ymax = [min(dec[:]), max(dec[:])]
            xfac, yfac = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
            left, right = xmin - xfac, xmax+xfac
            bottom, top = ymin-yfac, ymax+yfac

            low, high = wrg
            xmapper = LinearColorMapper(palette=my_palette,
                                        low=low, 
                                        high=high,
                                        nan_color="darkgrey")

            wmapper = LinearColorMapper(palette=my_palette,
                                        low= low,
                                        high= high,
                                        nan_color="darkgrey")

            # ============
            # XSIGMA WEDGE

            radius = 0.0165 
            radius_hover = 0.02

            # centralize wedges in plots:
            ra_center=0.5*(max(ra)+min(ra))
            dec_center=0.5*(max(dec)+min(dec))
            xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
            yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

            wedge_plot_x = Plot2d(
                x_range=xrange_wedge,
                y_range=yrange_wedge,
                x_label="RA",
                y_label="DEC",
                tooltip=xsigma_tooltip,
                title="XSIGMA",
                width=500,
                height=380,
                yscale="auto"
            ).wedge(
                source,
                x='x1',
                y='y1',
                field='delta_xsigma',
                mapper=xmapper,
                colorbar_title='xsigma'
            ).plot

            taptool = wedge_plot_x.select(type=TapTool)
            taptool.callback = OpenURL(url=url)

            # ============
            # WSIGMA WEDGE
            wedge_plot_w = Plot2d(
                x_range=xrange_wedge,
                y_range=yrange_wedge,
                x_label="RA",
                y_label="DEC",
                tooltip=wsigma_tooltip,
                title="WSIGMA",
                width=500,
                height=380,
                yscale="auto"
            ).wedge(
                source,
                x='x1',
                y='y1',
                field='delta_wsigma',
                mapper=wmapper,
                colorbar_title='wsigma'
            ).plot

            taptool = wedge_plot_w.select(type=TapTool)
            taptool.callback = OpenURL(url=url)

        # ================================
        # Stat histogram

        # x_fiber_hist
        d_yplt = (max(xsigma) - min(xsigma))*0.1
        yrange = [0, max(xsigma) + d_yplt]

        xhist = Plot2d(
            yrange,
            x_label="Fiber number",
            y_label="X std dev (number of pixels)",
            tooltip=xsigma_tooltip,
            title="",
            width=600,
            height=300,
            yscale="auto",
            hover_mode="vline",
        ).quad(
            source,
            top='xsigma',
        )

        # w_fiber_hist
        d_yplt = (max(wsigma) - min(wsigma))*0.1
        yrange = [0, max(wsigma) + d_yplt]

        whist = Plot2d(
            yrange,
            x_label="Fiber number",
            y_label="W std dev (number of pixels)",
            tooltip=xsigma_tooltip,
            title="",
            width=600,
            height=300,
            yscale="auto",
            hover_mode="vline",
        ).quad(
            source,
            top='wsigma',
        )

        # ================================
        # Stat histogram

        def histpar(yscale, hist):
            if yscale == 'log':
                ylabel = "Frequency + 1"
                yrange = (1, 11**(int(np.log10(max(hist)))+1))
                bottomval = 'bottomplusone'
                histval = 'histplusone'
            else:
                ylabel = "Frequency"
                yrange = (0.0*max(hist), 1.1*max(hist))
                bottomval = 'bottom'
                histval = 'hist'
            return [ylabel, yrange, bottomval, histval]


        xhistlabel = "XSIGMA"
        yscale = "auto"

        hist_tooltip_x = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Frequency: </span>
                    <span style="font-size: 1vw; color: #515151">@hist</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">XSIGMA: </span>
                    <span style="font-size: 1vw; color: #515151;">[@left, @right]</span>
                </div>
            </div>
        """

        hist, edges = np.histogram(xsigma, 'sqrt')

        source_hist = ColumnDataSource(data={
            'hist': hist,
            'histplusone': hist+1,
            'bottom': [0] * len(hist),
            'bottomplusone': [1]*len(hist),
            'left': edges[:-1],
            'right': edges[1:]
        })

        ylabel, yrange, bottomval, histval = histpar(yscale, hist)

        p_hist_x = Plot2d(
            x_label=xhistlabel,
            y_label=ylabel,
            tooltip=hist_tooltip_x,
            title="",
            width=600,
            height=300,
            yscale="auto",
            y_range=yrange,
            x_range=(hist_rg[0]+xw_ref[0],
                     hist_rg[1]+xw_ref[0]),
            hover_mode="vline",
        ).quad(
            source_hist,
            top=histval,
            bottom=bottomval,
            line_width=0.4,
        )

        # Histogram 2
        xhistlabel = "WSIGMA"
        hist_tooltip_w = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Frequency: </span>
                    <span style="font-size: 1vw; color: #515151">@hist</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">WSIGMA: </span>
                    <span style="font-size: 1vw; color: #515151;">[@left, @right]</span>
                </div>
            </div>
        """

        hist, edges = np.histogram(wsigma, 'sqrt')

        source_hist = ColumnDataSource(data={
            'hist': hist,
            'histplusone': hist+1,
            'bottom': [0] * len(hist),
            'bottomplusone': [1]*len(hist),
            'left': edges[:-1],
            'right': edges[1:]
        })

        ylabel, yrange, bottomval, histval = histpar(yscale, hist)
        yrangew = yrange

        p_hist_w = Plot2d(
            x_label=xhistlabel,
            y_label=ylabel,
            tooltip=hist_tooltip_w,
            title="",
            width=600,
            height=300,
            yscale="auto",
            y_range=yrange,
            x_range=(hist_rg[0]+xw_ref[1],
                     hist_rg[1] + xw_ref[1]),
            hover_mode="vline",
        ).quad(
            source_hist,
            top=histval,
            bottom=bottomval,
            line_width=0.8,
        )

        # --------------------------------------------------------------
        # vlines ranges:
        bname = 'XWSIGMA'

        for ialert in nrg:  # par[bname+'_NORMAL_RANGE']:
            spans = Span(location=ialert+xw_ref[0], 
                        dimension='height',
                        line_color='green',
                        line_dash='dashed', line_width=2)
            p_hist_x.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[0], 
                            y= yrange[-1]/2.2,
                            y_units='data',
                            text='Normal',
                            text_color='green', angle=np.pi/2.)
            p_hist_x.add_layout(my_label)

        for ialert in wrg:  # par[bname+'_WARN_RANGE']:
            spans = Span(location=ialert+xw_ref[0], dimension='height', line_color='tomato',
                         line_dash='dotdash', line_width=2)
            p_hist_x.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[0], y=yrange[-1]/2.2, y_units='data',
                             text='Warning', text_color='tomato', angle=np.pi/2.)
            p_hist_x.add_layout(my_label)

        for ialert in nrg:  # par[bname+'_NORMAL_RANGE']:
            spans = Span(location=ialert+xw_ref[1], dimension='height', line_color='green',
                         line_dash='dashed', line_width=2)
            p_hist_w.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[1], y=yrangew[-1]/2.2, y_units='data',
                             text='Normal', text_color='green', angle=np.pi/2.)
            p_hist_w.add_layout(my_label)

        for ialert in wrg:  # par[bname+'_WARN_RANGE']:
            spans = Span(location=ialert+xw_ref[1], dimension='height', line_color='tomato',
                         line_dash='dotdash', line_width=2)
            p_hist_w.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[1], y=yrangew[-1]/2.2, y_units='data',
                             text='Warning', text_color='tomato', angle=np.pi/2.)
            p_hist_w.add_layout(my_label)


        # amp 1
        xamp = Patch().plot_amp(
            dz=xw_amp[0],
            refexp=[xw_ref[0]]*4,
            name="XSIGMA AMP",
            description="X standard deviation (number of pixels)",
            wrg=wrg
        )

        xamp_status = Patch().plot_amp(
            dz=xw_amp[0],
            refexp=[xw_ref[0]]*4,
            name="XSIGMA AMP (STATUS)",
            description="X standard deviation (number of pixels)",
            wrg=wrg,
            nrg=nrg,
            status_plot=True,
        )

        # amp 2
        wamp = Patch().plot_amp(
            dz=xw_amp[1],
            refexp=[xw_ref[1]]*4,
            name="WSIGMA AMP",
            description="W standard deviation (number of pixels)",
            wrg=wrg
        )

        wamp_status = Patch().plot_amp(
            dz=xw_amp[1],
            refexp=[xw_ref[1]]*4,
            name="WSIGMA AMP (STATUS)",
            description="W standard deviation (number of pixels)",
            wrg=wrg,
            nrg=nrg,
            status_plot=True,
        )

        # -------------------------------------------------------------------------
        info_col = Title().write_description('xwsigma')

        current_exposures = check_ccds['METRICS']['XWSIGMA']

        if flavor == 'science':
            program = gen_info['PROGRAM'].upper()
            reference_exposures = check_ccds['PARAMS']['XWSIGMA_' + program + '_REF']
            keynames = ["XSIGMA"]
            table_x = Table().single_table(keynames, [current_exposures[0]], 
                [reference_exposures[0]], nrg, wrg)
            keynames = ["WSIGMA"]
            table_w = Table().single_table(keynames,  [current_exposures[1]], 
                [reference_exposures[1]], nrg, wrg)

            layout = column(
                info_col,
                widgetbox(Div(), css_classes=["tableranges"]),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  XSIGMA </h2>')),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  WSIGMA </h2>')),
                table_x,
                table_w,
                column(wedge_plot_x, sizing_mode='scale_both'),
                column(wedge_plot_w, sizing_mode='scale_both'),
                column(xhist, sizing_mode='scale_both'),
                column(whist, sizing_mode='scale_both'),
                column(p_hist_x, sizing_mode='scale_both'),
                column(p_hist_w, sizing_mode='scale_both'),
                column(xamp, sizing_mode='scale_both'),
                column(wamp, sizing_mode='scale_both'),
                column(xamp_status, sizing_mode='scale_both'),
                column(wamp_status, sizing_mode='scale_both'),
                css_classes=["display-grid"], sizing_mode='scale_width')
        else:
            reference_exposures = check_ccds['PARAMS']['XWSIGMA_REF']
            keynames = ["XSIGMA"]
            table_x = Table().single_table(keynames, current_exposures, 
                reference_exposures, nrg, wrg)
            keynames = ["WSIGMA"]
            table_w = Table().single_table(keynames, current_exposures, 
                reference_exposures, nrg, wrg)

            layout = column(
                info_col,
                widgetbox(Div(), css_classes=["tableranges"]),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  XSIGMA </h2>')),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  WSIGMA </h2>')),
                table_x,
                table_w,
                column(xhist, sizing_mode='scale_both'),
                column(whist, sizing_mode='scale_both'),
                column(p_hist_x, sizing_mode='scale_both'),
                column(p_hist_w, sizing_mode='scale_both'),
                column(xamp, sizing_mode='scale_both'),
                column(wamp, sizing_mode='scale_both'),
                column(xamp_status, sizing_mode='scale_both'),
                column(wamp_status, sizing_mode='scale_both'),
               
                css_classes=["display-grid"], sizing_mode='scale_width')
           
        return file_html(layout, CDN, "XWSIGMA")
