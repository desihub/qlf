from bokeh.models.widgets import Div
from bokeh.layouts import widgetbox
import numpy as np

class Table:
    def validate_array_size(self, array, size):
        if len(array) < size:
            for i in range(size-len(array)):
                array.append(np.nan)

    def single_table(self, keynames, current_exposures, reference_exposures, nrg, wrg ):
        self.validate_array_size(current_exposures, len(keynames))
        self.validate_array_size(reference_exposures, len(keynames))
        style = """    <style>        table {
                font-family: arial, sans-serif;
                font-size: 1.2vw;
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
            <div  style="text-align:center;padding-left:10px;padding-top:10px;">
            <table>
                <col width="120">
                <col width="80">
                <col width="80">
                <col width="80">
            </tr>
            <tr>
                <th>Keyname</th> <th>Current</th> <th>Normal</th> <th>Warning</th>
            </tr>"""

        tblines=""
        for i, keyname in enumerate(keynames):
            tblines = tblines +\
                """<tr>
                    <td>{}</td> <td>{}</td> <td>  {} &ndash;  {} </td> <td>  {} &ndash;  {} </td>
                    </tr>
                        """.format(keyname, 
                            round(current_exposures[i], 2), 
                            round(nrg[0]+ reference_exposures[i], 2), round(nrg[1]+ reference_exposures[i], 2), 
                            round(wrg[0]+ reference_exposures[i], 2), round(wrg[1]+ reference_exposures[i], 2), )

        end = """</table> </div> """

        table = style + header + tblines + end
        return widgetbox(Div(text=table))

