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

    def validate_array_size(self, array, size):
        if len(array) < size:
            for i in range(size-len(array)):
                array.append(np.nan)

    def reference_table(self, keynames, current_exposures, reference_exposures):
        self.validate_array_size(current_exposures, len(keynames))
        self.validate_array_size(reference_exposures, len(keynames))
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

        tblines=""
        for i, keyname in enumerate(keynames):
            tblines = tblines +\
                """<tr>
                            <td>{}</td> <td>{}</td> <td>{}</td>
                            </tr>
                            """.format(keyname, round(current_exposures[i], 2), round(reference_exposures[i], 2))

        end = """</table> </div> """

        table = style + header + tblines + end
        return widgetbox(Div(text=table))
