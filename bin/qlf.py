import sys
import time
import requests

class QLFApp():

    def mkconfig(self):
        # TODO: Make QL configuration
        pass

    def run(self):

        print("Starting QLF daemon...")
        while True:
            # TODO: Call the QL pipeline here
            # For now, just assume a constant value for the SNR measurement each 10 sec

            job = {"name": "QL", "status": 0, "measurements": [{"metric": "SNR", "value": 1.0}]}
            time.sleep(10)

            # Send measurement results
            self.post(job)

    def post(self, job):

        try:
            api = requests.get('http://localhost:8000/dashboard/api/').json()
            response = requests.post(api['job'], json=job, auth=("nobody", "nobody"))
        except:
            print('QLF API is not responding, restart QLF.')
            sys.exit(1)

if __name__ == "__main__":

    app = QLFApp()
    app.run()
