from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool

from bokeh.models.widgets import Select, Div, Slider
from bokeh.layouts import row, widgetbox, column, gridplot
from defaults import init_xy_plot
from service import get_plot_data


class Metrics(object):
    """The metrics app consists of a time series plot showing measurements
    for a given selected dataset and metric.
    """

    def __init__(self):

        # app title
        self.title = Div(text=self.make_title("Spectral signal-to-noise", ""))
        # data store values consumed by the app
        self.data = {}

        # the column data sources store values displayed by bokeh plots

        self.elg = ColumnDataSource(data={'mag': [],
                                          'snr': [],
                                          'spectrograph': [],
                                          'fiber_id': []})

        self.lrg = ColumnDataSource(data={'mag': [],
                                          'snr': [],
                                          'spectrograph': [],
                                          'fiber_id': []})

        self.qso = ColumnDataSource(data={'mag': [],
                                          'snr': [],
                                          'spectrograph': [],
                                          'fiber_id': []})

        self.star = ColumnDataSource(data={'mag': [],
                                           'snr': [],
                                           'spectrograph': [],
                                           'fiber_id': []})

        self.compose_layout()

    def compose_layout(self):
        """Compose the app layout, the main elements are the widgets to
        select the metric a div for the title and a plot
        """

        # slider is used to select the exposure
        self.slider = Slider(start=1, end=10, value=1, step=1,
                             title="Exposure ID")

        # we also can select the spectrograph
        spectrograph = Select(title="Spectrograph:",
                              value='0',
                              options=['All', '0', '1', '2', '3', '4',
                                       '5', '6', '7', '8', '9'],
                              width=100)

        # and the arm
        arm = Select(title="Arm:",
                     value='r',
                     options=['b', 'r', 'z'],
                     width=100)

        self.data = get_plot_data()

        self.update_data_source()

        self.make_snr_plots()

        self.layout = column(widgetbox(self.title, width=500),
                             widgetbox(self.slider, width=1000),
                             row(widgetbox(arm, width=150),
                                 widgetbox(spectrograph, width=150)),
                             self.plot)

    # TODO: this method can be used as example to handle events

    def on_exposure_change(self, attr, old, new):
        """Handle exposure select event,  it updates the plot when another
         exposure is selected

        Parameters
        ----------
        attr : str
            refers to the changed attribute’s name, not used
        old : str
            previous value, not used
        new : str
            new value

        See also
        --------
        http://bokeh.pydata.org/en/latest/docs/user_guide/interaction
        /widgets.html#userguide-interaction-widgets
        """

        # update plot labels
        self.plot.yaxis.axis_label = new

        self.selected_exposure = new

        self.data = get_plot_data(new)

        self.update_data_source()

    def update_data_source(self):
        """Update the bokeh data source with measurements for the selected
        dataset and metric
        """

        # all attributes of a data source must have the same size

        size = len(self.data['elg_mag'])
        spectrograph = ['0'] * size

        self.elg.data = dict(mag=self.data['elg_mag'],
                             snr=self.data['elg_snr'],
                             spectrograph=spectrograph,
                             fiber_id=self.data['elg_fiber_id'],)

        size = len(self.data['lrg_mag'])
        spectrograph = ['0'] * size

        self.lrg.data = dict(mag=self.data['lrg_mag'],
                             snr=self.data['lrg_snr'],
                             spectrograph=spectrograph,
                             fiber_id=self.data['lrg_fiber_id'],)

        size = len(self.data['qso_mag'])
        spectrograph = ['0'] * size

        self.qso.data = dict(mag=self.data['qso_mag'],
                             snr=self.data['qso_snr'],
                             spectrograph=spectrograph,
                             fiber_id=self.data['qso_fiber_id'],)

        size = len(self.data['star_mag'])
        spectrograph = ['0'] * size

        self.star.data = dict(mag=self.data['star_mag'],
                              snr=self.data['star_snr'],
                              spectrograph=spectrograph,
                              fiber_id=self.data['star_fiber_id'],)

        # Plot title and description must be updated too
        # title = "{}".format(self.selected_metric)
        # description = self.metrics['description'][self.selected_metric]
        # description = ""
        # self.title.text = self.make_title(title, description)

    def make_title(self, title, description):
        """ Update page title with the selected metric
        """
        return """<left><h2>{}</h2>{}
        </left>""".format(title, description)

    def make_snr_plots(self):

        hover = HoverTool(tooltips=[("Spectrograph", "@spectrograph"),
                                    ("Fiber ID", "@fiber_id"),
                                    ("Value", "@snr")])

        elg = init_xy_plot(hover=hover)

        elg.circle(x='mag', y='snr', source=self.elg,
                   color="blue", size=3)

        elg.xaxis.axis_label = "DECAM_R"
        elg.yaxis.axis_label = "SNR"
        elg.title.text = "ELG"

        hover = HoverTool(tooltips=[("Spectrograph", "@spectrograph"),
                                    ("Fiber ID", "@fiber_id"),
                                    ("Value", "@snr")])

        lrg = init_xy_plot(hover=hover)

        lrg.circle(x='mag', y='snr', source=self.lrg,
                   color="red", size=3)

        lrg.xaxis.axis_label = "DECAM_R"
        lrg.yaxis.axis_label = "SNR"
        lrg.title.text = "LRG"

        hover = HoverTool(tooltips=[("Spectrograph", "@spectrograph"),
                                    ("Fiber ID", "@fiber_id"),
                                    ("Value", "@snr")])

        qso = init_xy_plot(hover=hover)

        qso.circle(x='mag', y='snr', source=self.qso,
                   color="green", size=3)

        qso.xaxis.axis_label = "DECAM_R"
        qso.yaxis.axis_label = "SNR"
        qso.title.text = "QSO"

        hover = HoverTool(tooltips=[("Spectrograph", "@spectrograph"),
                                    ("Fiber ID", "@fiber_id"),
                                    ("Value", "@snr")])

        star = init_xy_plot(hover=hover)
        star.circle(x='mag', y='snr', source=self.star,
                    color="black", size=3)

        star.xaxis.axis_label = "DECAM_R"
        star.yaxis.axis_label = "SNR"
        star.title.text = "STAR"

        self.plot = gridplot([[elg,lrg],[qso,star]])


curdoc().add_root(Metrics().layout)
curdoc().title = "Quick Look"
