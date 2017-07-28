from bokeh.plotting import curdoc, figure
from bokeh.models.widgets import Select
from bokeh.layouts import widgetbox, row, column
from dashboard.bokeh.helper import get_exposures
from bokeh.models import Div, Panel, Tabs

# Get the list of exposures
exposures = get_exposures()

x = exposures['ra']
y = exposures['dec']

plot = figure(tools='pan,box_zoom,reset')

plot.circle(x, y, size=8)

plot.xaxis.axis_label = "RA (deg)"
plot.yaxis.axis_label = "DEC (deg)"

select = Select(title="Program:", value="All", options=["All", "Dark", "Grey", "Bright"])

panel_exposures = row(column(Div(text="<b>N Exposures:</b> {}".format(str(len(x)))), widgetbox(select)), column(plot))

tab = Panel(child=panel_exposures, title="Footprint")

curdoc().add_root(Tabs(tabs=[tab]))
curdoc().title = "Footprint"
