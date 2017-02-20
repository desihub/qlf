import sys
import time

from qlf_daemon.qlf_ingest import post


class QLFApp():

    def mkconfig(self):
        # TODO: Generate the QL configuration file
        pass

    def run(self):

        print("Starting QLF daemon...")
        while True:
            # TODO: Call the QL pipeline here
            try:
                # Send QA results to the QLF database
                # For now read test data each 10s
                time.sleep(10)
                post('../test/data/qa-snr-r0-00000000.yaml')
            except:
                print('QLF is not responding, please restart.')
                sys.exit(1)

if __name__ == "__main__":

    app = QLFApp()
    app.run()
