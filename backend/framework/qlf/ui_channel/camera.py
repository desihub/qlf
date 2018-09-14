class Camera:
    def __init__(self, name):
        self.name = name
        self.step = None
        self.steps_status = ['none', 'none', 'none', 'none']
        self.steps_list = ['preproc', 'extract', 'fiberfl', 'skysubs']

        self.steps_dic = {
            'preproc': ['countpix', 'getbias', 'getrms', 'xwsigma'],
            'extract': ['countbins'],
            'fiberfl': ['skycont', 'skypeak'],
            'skysubs': ['skyresid', 'integ', 'snr'],
        }

        self.alert_keys = {
            'NOISE_STATUS': 'getrms',
            'LITFRAC_STATUS': 'countpix',
            'BIAS_STATUS': 'getbias',
            'NGOODFIB_STATUS': 'countbins',
            'DELTAMAG_STATUS': 'integ',
            'XWSIGMA_STATUS': 'xwsigma',
            'FIDSNR_STATUS': 'snr',
            'SKYCONT_STATUS': 'skycont',
            'PEAKCOUNT_STATUS': 'skypeak',
            'RESID_STATUS': 'skyresid',
        }


        self.qas_status = {
            'preproc': {'steps_status': ['None', 'None', 'None', 'None']},
            'extract': {'steps_status': ['None']},
            'fiberfl': {'steps_status': ['None', 'None']},
            'skysubs': {'steps_status': ['None', 'None', 'None']},
        }

    def get_qa_status(self, key):
        selected_qa = self.alert_keys[key]
        for step in self.steps_dic:
            if selected_qa in self.steps_dic[step]:
                selected_step = step
                qa_index = self.steps_dic[step].index(selected_qa)
        return self.qas_status[selected_step]['steps_status'][qa_index]

    def set_qa_status(self, key, status):
        selected_qa = self.alert_keys[key]
        for step in self.steps_dic:
            if selected_qa in self.steps_dic[step]:
                selected_step = step
                qa_index = self.steps_dic[step].index(selected_qa)
        self.qas_status[selected_step]['steps_status'][qa_index] = status

    def set_step_status(self, step, status):
        status_index = self.steps_list.index(step)
        self.steps_status[status_index] = status

    def get_step_status(self, step):
        status_index = self.steps_list.index(step)
        return self.steps_status[status_index]


if __name__ == "__main__":
    cam = Camera('b0')



