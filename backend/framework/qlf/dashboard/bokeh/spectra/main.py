from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HoverTool

from bokeh.resources import CDN
from bokeh.embed import file_html
import os

from astropy.io import fits

# ----------------------------
# READ FROM INTERFACE:
# Instance of fiber_ID & spectrograph:
fid=2 
spectrograph="0"
selected_arm=['b']

qlf_root = os.environ.get('QLF_ROOT')

class Spectra():
    def __init__(self, camera):
        self.camera = camera
        # self.models = QLFModels()

    def load_frame(self, fiber_id):
        frame=fits.open("{}/spectro/redux/exposures/20191001/00003578/sframe-{}-00003578.fits""".format(qlf_root, self.camera))   
        flux =frame["FLUX"].data
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

    def render(self):
        # -----------------------
        # Bokeh pre-configuration:
        color={'b':"dodgerblue","r":"red", "z":"magenta"}
        hover_color={'b':"red","r":"darkblue", "z":"darkblue"}
        spec_tooltip = """
                        <div>
                            <div>
                                <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
                                <span style="font-size: 13px; color: #515151">@wlength &#8491</span>
                            </div>
                            <div>
                                <span style="font-size: 12px; font-weight: bold; color: #303030;">Counts: </span>
                                <span style="font-size: 13px; color: #515151;">@spec</span>
                            </div>
                        </div>
                    """
        spec_hover = HoverTool(tooltips=spec_tooltip, mode='vline', names=['bar'])


        # -------------------
        # Saving ploting data:
        fluxes = {}
        for arm in selected_arm:
            fl=self.load_frame(fid)
            fluxes.update({arm:fl})

        for arm in [list(fluxes.keys())[0]]:
            brick= fluxes[arm]['brick']
            obj_name= fluxes[arm]['otype']


        # ------------
        # Bokeh Plots:
        p_spec = Figure(title="Brick name: "+brick+',  Fiber ID: %d' % fid,
                        x_axis_label= 'Wavelength (A)', 
                        y_axis_label= obj_name+' Flux (counts)',
                        plot_width=800, plot_height=340,
                        active_drag="box_zoom",
                        tools=[spec_hover, "pan,box_zoom,reset,crosshair, wheel_zoom"], sizing_mode='scale_width')

        for arm in fluxes.keys():
            spec_source=ColumnDataSource(data={'wlength': fluxes[arm]['wl'],
                                            'spec': fluxes[arm]['flux'],
                                            })

            p_spec.line('wlength', 'spec', color=color[arm],
                        source=spec_source,)
            p_spec.vbar('wlength', top='spec',
                        width=1., source=spec_source,
                        name="bar",
                        color=None,hover_color=hover_color[arm])

        # -----------    
        # Formatting:    
        font_size="1.1vw"
        for plot in [p_spec]:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size

        return file_html(p_spec, CDN, "Spectra")