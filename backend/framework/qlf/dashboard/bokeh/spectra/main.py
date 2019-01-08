from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import HoverTool, ColumnDataSource, Range1d, TapTool
from bokeh.models.callbacks import CustomJS
from dashboard.models import Process, Fibermap, Job
from qlf_models import QLFModels
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Button
from bokeh.resources import CDN
from bokeh.embed import file_html
import os

from astropy.io import fits

qlf_root = os.environ.get('QLF_ROOT')
spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')


class Spectra():
    def __init__(self, process_id, arms):
        self.selected_process_id = process_id
        self.process = Process.objects.get(pk=process_id)
        exposure = self.process.exposure
        self.exposure = exposure
        self.selected_arm = arms

    def data_source(self, fmap):
        """ Creating data source for plots
        """
        data_model = {
            'fiber': [],
            'color': [],
            'cam': [],
            'OBJ_TYPE': [],
            'ra':  [],
            'dec': [],
        }

        ra_tile = fmap.fiber_ra
        dec_tile = fmap.fiber_dec
        otype_tile = fmap.objtype

        y = []
        color = []
        cam_inst = []
        for spec in list(range(10)):
            sframe_exists = False
            for arm in self.selected_arm:
                cam = arm+str(spec)
                process_dir = self.process.process_dir
                path_exists = os.path.isfile("{}/{}/sframe-{}-{}.fits""".format(
                    spectro_redux,
                    process_dir,
                    cam,
                    process_dir.split('/')[-1],
                ))
                if path_exists:
                    sframe_exists = True

            if sframe_exists:
                y = y + list(range(500))
                color = color + ['green']*500
            else:
                y = y + list(range(500))
                color = color + ['lightgray']*500

            cam_inst = cam_inst + [cam]*500

            data_model['fiber'] = y
            data_model['color'] = color
            data_model['cam'] = cam_inst

            data_model['OBJ_TYPE'] = otype_tile
            data_model['ra'] = ra_tile
            data_model['dec'] = dec_tile

        source = ColumnDataSource(data=data_model)

        return source

    def wedge_plot(self, wedge_arm, fmap, common_source=None):
        ra_center = fmap.exposure.telra
        dec_center = fmap.exposure.teldec

        fiber_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER: </span>
                    <span style="font-size: 1.1vw; color: #515151">@fiber</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1.1vw; color: #515151;">@ra</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 1.1vw; color: #515151;">@dec</span>
                </div>
        """

        hover = HoverTool(tooltips=fiber_tooltip)

        source = common_source

        radius = 0.017
        radius_hover = 0.018
        plot_space = 0.1

        xrange = Range1d(
            start=min(source.data['ra'])-plot_space, end=max(source.data['ra'])+plot_space)
        yrange = Range1d(start=min(
            source.data['dec'])-plot_space, end=max(source.data['dec'])+plot_space)

        p = figure(title='FIBERS (ARM %s)' % (','.join(wedge_arm)),
                   x_axis_label='RA',
                   y_axis_label='DEC',
                   plot_width=600,
                   plot_height=600,
                   tools=[
                       hover, "box_zoom,pan,wheel_zoom,reset,lasso_select,crosshair,tap"],
                   active_drag="box_zoom",
                   sizing_mode='scale_width',
                   x_range=xrange,
                   y_range=yrange)
        p.title.align = 'center'

        p.circle('ra', 'dec', source=source, name="data", radius=radius,
                 fill_color={'field': 'color'},
                 line_color='black', line_width=0.4,
                 hover_line_color='red')

        p.circle('ra', 'dec', source=source, name="data", radius=radius_hover,
                 hover_fill_color={'field': 'color'}, fill_color=None,
                 line_color=None, line_width=3, hover_line_color='red')

        taptool = p.select(type=TapTool)
        taptool.callback = CustomJS(args=dict(source=source), code="""
            const selected = source.selected['1d']['indices'][0];
            const fiber = source.data['fiber'][selected]
            const camera = source.data['cam'][selected]
            const color = source.data['color'][selected]
            const data = {
                "fiber": fiber,
                "camera": camera
            };
            if (color !== 'lightgray')
              window.parent.postMessage(data, '*');
        """)

        return p

    def load_spectra(self):
        fmap = Fibermap.objects.filter(exposure=self.exposure)[0]

        src = self.data_source(fmap)

        p = self.wedge_plot(self.selected_arm, fmap, common_source=src)
        layout = row(p, sizing_mode='scale_width')

        return file_html(layout, CDN, "Spectra")

    def load_frame(self, fiber_id, arm):
        try:
            process_dir = self.process.process_dir
            frame_path = "{}/{}/sframe-{}-{}.fits""".format(
                spectro_redux,
                process_dir,
                arm+self.spectrograph,
                process_dir.split('/')[-1],
            )
            frame = fits.open(frame_path)
        except:
            return None
        flux = frame["FLUX"].data
        wl = frame["WAVELENGTH"].data
        otype = frame['FIBERMAP'].data['OBJTYPE']
        fmap = frame["FIBERMAP"].data
        return dict(
            flux=flux[fiber_id],
            wl=wl,
            otype=otype[fiber_id],
            ra=fmap['RA_OBS'][fiber_id],
            dec=fmap['DEC_OBS'][fiber_id],
            fid=fiber_id,
            brick=fmap['BRICKNAME'][fiber_id],)

    def render_spectra(self, fiber, spectrograph):
        fiber = int(fiber)
        self.spectrograph = spectrograph
        # -----------------------
        # Bokeh pre-configuration:
        color = {'b': "dodgerblue", "r": "red", "z": "magenta"}
        hover_color = {'b': "red", "r": "darkblue", "z": "darkblue"}
        spec_tooltip = """
                        <div>
                            <div>
                                <span style="font-size: 1vw; font-weight: bold; color: #303030;">Wavelength: </span>
                                <span style="font-size: 1.1vw; color: #515151">@wlength &#8491</span>
                            </div>
                            <div>
                                <span style="font-size: 1vw; font-weight: bold; color: #303030;">Counts: </span>
                                <span style="font-size: 1.1vw; color: #515151;">@spec</span>
                            </div>
                        </div>
                    """
        spec_hover = HoverTool(tooltips=spec_tooltip,
                               mode='vline', names=['bar'])

        # -------------------
        # Saving ploting data:
        fluxes = {}
        ra_obs = ''
        dec_obs = ''
        for arm in self.selected_arm:
            fl = self.load_frame(fiber, arm)
            if fl:
                fluxes.update({arm: fl})
                ra_obs = fl['ra']
                dec_obs = fl['dec']

        for arm in [list(fluxes.keys())[0]]:
            brick = fluxes[arm]['brick']
            obj_name = fluxes[arm]['otype']

        # ------------
        # Bokeh Plots:
        p_spec = figure(title="Brick name: "+brick+',  Fiber ID: %d, RA: %.2f, DEC: %.2f' % (fiber, ra_obs, dec_obs),
                        x_axis_label='Wavelength (A)',
                        y_axis_label=obj_name+' Flux (counts)',
                        plot_width=800, plot_height=340,
                        active_drag="box_zoom",
                        tools=[spec_hover, "pan,box_zoom,reset,crosshair, wheel_zoom"], sizing_mode='scale_width')

        for arm in fluxes.keys():
            spec_source = ColumnDataSource(data={'wlength': fluxes[arm]['wl'],
                                                 'spec': fluxes[arm]['flux'],
                                                 })

            p_spec.line('wlength', 'spec', color=color[arm],
                        source=spec_source,)
            p_spec.vbar('wlength', top='spec',
                        width=1., source=spec_source,
                        name="bar",
                        color=None, hover_color=hover_color[arm])

        # -----------
        # Formatting:
        font_size = "1.1vw"
        for plot in [p_spec]:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size

        callback = CustomJS(code="""
                    data={'back': true}
                    window.parent.postMessage(data, '*');
                """)

        button = Button(label="Back", button_type="warning", callback=callback)

        layout = column(p_spec, widgetbox(button), sizing_mode='scale_width')
        return file_html(layout, CDN, "Spectra")
