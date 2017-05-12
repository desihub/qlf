# import sys
# import time
# import os
# import configparser

from dos_monitor import DOSmonitor
from qlf_pipeline import QLFPipeline

class QLFApp():

    def run(self):

        # TODO: make daemon
        dosmonitor = DOSmonitor()
        night = dosmonitor.get_last_night()
        exposures = dosmonitor.get_exposures_by_night(night)

        for exposure in exposures:
            qlp = QLFPipeline(exposure)
            qlp.start_process()

        # print("Starting QLF daemon...")
        #
        # while True:
        #     # TODO: Call the QL pipeline here
        #     try:
        #         # Send QA results to the QLF database
        #         # For now read test data each 10s
        #         time.sleep(10)
        #         post('../test/data/qa-snr-r0-00000000.yaml')
        #     except:
        #         print('QLF is not responding, please restart.')
        #         sys.exit(1)

if __name__ == "__main__":

    app = QLFApp()
    app.run()
