class Camera:
    def __init__(self, name, stages):
        self.name = name
        self.step = None

        self.steps_dic = dict()
        self.qas_status = dict()
        self.alert_keys = dict()
        self.steps_status = list()
        for step in stages['step_list']:
            self.steps_status.append('none')
            self.steps_dic[step['name']] = list()
            self.qas_status[step['name']] = list()
            for qa in step['qa_list']:
                self.steps_dic[step['name']].append(qa['name'])
                self.qas_status[step['name']].append('None')
                self.alert_keys[qa['status_key']] = qa['name']

    def get_qa_status(self, key):
        selected_qa = self.alert_keys[key]
        for step in self.steps_dic:
            if selected_qa in self.steps_dic[step]:
                selected_step = step
                qa_index = self.steps_dic[step].index(selected_qa)
        return self.qas_status[selected_step][qa_index]

    def set_qa_status(self, key, status):
        selected_qa = self.alert_keys[key]
        for step in self.steps_dic:
            if selected_qa in self.steps_dic[step]:
                selected_step = step
                qa_index = self.steps_dic[step].index(selected_qa)
        self.qas_status[selected_step][qa_index] = status

    def set_step_status(self, step, status):
        status_index = list(self.steps_dic).index(step)
        self.steps_status[status_index] = status

    def get_step_status(self, step):
        status_index = list(self.steps_dic).index(step)
        return self.steps_status[status_index]


if __name__ == "__main__":
    cam = Camera('b0')
