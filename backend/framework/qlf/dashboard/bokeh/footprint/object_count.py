import os
from dashboard.models import Job, Process, Fibermap
from qlf_models import QLFModels
import pandas as pd

spectro_data = os.environ.get('DESI_SPECTRO_DATA')


class ObjectStatistics:
    def __init__(self, process_id):
        self.selected_process_id = process_id

    def generate_statistics(self):
        # Load fibermap
        process_id = self.selected_process_id
        process = Process.objects.get(pk=process_id)
        joblist = [entry.camera.camera for entry in
                   Job.objects.filter(process_id=process_id)]
        exposure = process.exposure
        fmap = Fibermap.objects.filter(exposure=exposure)[0]

        # Object Statistics from fmap:
        objects = fmap.objtype

        obj_stat_dict = {}
        list_of_obj = ['TGT', 'STAR']

        speclist = set([int(x[-1]) for x in joblist])
        obj_spec = [objects[i*500:(i+1)*500] for i in speclist]
        obj_spec = [i for ob in obj_spec for i in ob]

        for o in list_of_obj:
            if o not in set(obj_spec):
                count = 0
            else:
                count = obj_spec.count(o)

            obj_stat_dict.update({o: count})

        #####################################################
        # Classification
        # Questions: objects defined by cam (arm+spectrograph)!
        # this means 15.000 per exposition
        # Their status may be different per arm

        col_stat = []
        col_ntgt = []
        col_nstar = []

        # Creating columns for snr df
        for cam in [arm+str(spec) for arm in ['b', 'r', 'z'] for spec in list(range(10))]:
            arm = int(cam[-1])
            col_ntgt.append(objects[arm*500: (arm+1)*500].count('TGT'))
            col_nstar.append(objects[arm*500: (arm+1)*500].count('STAR'))

            if cam in joblist:
                mergedqa = QLFModels().get_output(
                    self.selected_process_id, cam)
                status = mergedqa['TASKS']['CHECK_SPECTRA']['METRICS']['PEAKCOUNT_STATUS']
                col_stat.append(status)
            else:
                col_stat.append('n/a')

        df = pd.DataFrame({'cam': [arm+str(spec) for arm in ['b', 'r', 'z'] for spec in list(range(10))],
                           'snr_status': col_stat,
                           'TGT': col_ntgt,
                           'STAR': col_nstar})

        def check_df(qtype, qstatus, qa, qarm=None):
            """ Query in dataframe
            """
            if qarm == None:
                obj_statistics = df.loc[df[qa] == qstatus][qtype]
                return obj_statistics.sum()
            elif qarm in ['b', 'r', 'z']:
                armlist = [qarm+str(spec) for spec in list(range(10))]
                obj_statistics = df.loc[(df[qa] == qstatus)
                                        & (df['cam'].isin(armlist))][qtype]
                return obj_statistics.sum()
            else:
                return None

        # SNR classification for ALL arms:
        snr_class = {}
        for j in ['NORMAL', 'WARN', 'ALARM', 'n/a']:
            obj_class = {}
            for i in ['TGT',  'STAR']:
                obj_class.update({i: check_df(i, j, 'snr_status')})
            snr_class.update({j: obj_class})

        # SNR classification per EACH arm:
        snr_class_arm = {}
        for arm in ['b', 'r', 'z']:
            status_class = {}
            for j in ['NORMAL', 'WARN', 'ALARM', 'n/a']:
                obj_class = {}
                for i in ['TGT', 'STAR']:
                    obj_class.update(
                        {i: check_df(i, j, 'snr_status', qarm=arm)})
                status_class.update({j: obj_class})
            snr_class_arm.update({arm: status_class})

        # ===================
        #       Fiber df

        col_fiber = {'b': [], 'r': [], 'z': []}
        for arm in ['b', 'r', 'z']:
            arm_col = []
            for spec in list(range(10)):
                cam = arm+str(spec)
                if cam in joblist:
                    mergedqa = QLFModels().get_output(
                        self.selected_process_id, cam)
                    fiberstatus = mergedqa['TASKS']['CHECK_FIBERS']['METRICS']['GOOD_FIBERS']
                    arm_col = arm_col+fiberstatus
                else:
                    arm_col = arm_col + [-9999]*500

            # SNR classification for ALL arms:
            snr_class = {}
            for j in ['NORMAL', 'WARN', 'ALARM', 'n/a']:
                obj_class = {}
                for i in ['TGT', 'STAR']:
                    obj_class.update({i: check_df(i, j, 'snr_status')})
                snr_class.update({j: obj_class})

            # SNR classification per EACH arm:
            snr_class_arm = {}
            for arm in ['b', 'r', 'z']:
                status_class = {}
                for j in ['NORMAL', 'WARN', 'ALARM', 'n/a']:
                    obj_class = {}
                    for i in ['TGT', 'STAR']:
                        obj_class.update(
                            {i: check_df(i, j, 'snr_status', qarm=arm)})
                    status_class.update({j: obj_class})
                snr_class_arm.update({arm: status_class})

            # ===================
            #       Fiber df

            col_fiber = {'b': [], 'r': [], 'z': []}
            for arm in ['b', 'r', 'z']:
                arm_col = []
                for spec in list(range(10)):
                    cam = arm+str(spec)
                    if cam in joblist:
                        mergedqa = QLFModels().get_output(
                            self.selected_process_id, cam)
                        fiberstatus = mergedqa['TASKS']['CHECK_FIBERS']['METRICS']['GOOD_FIBERS']
                        arm_col = arm_col+fiberstatus
                    else:
                        arm_col = arm_col + [-9999]*500

                col_fiber.update({arm: arm_col})

            df_fiber = pd.DataFrame({**col_fiber, **{'object': objects}})

            def check_fibers(qtype, qstatus, qarm=None):
                """Fiber query"""
                if qstatus == 'GOOD':
                    stat = 1
                elif qstatus == 'BAD':
                    stat = 0
                elif qstatus == 'n/a':
                    stat = -9999
                else:
                    return None

                if qtype == 'STAR':
                    qtype = 'STD'

                if qarm == None:
                    count = 0
                    for i in ['b', 'r', 'z']:
                        obj_statistics = df_fiber.loc[(
                            df_fiber[i] == stat)]['object']
                        count += list(obj_statistics).count(qtype)
                    return count
                if qarm in ['b', 'r', 'z']:
                    obj_statistics = df_fiber.loc[(
                        df_fiber[qarm] == stat)]['object']
                    return list(obj_statistics).count(qtype)
                else:
                    return None

        df_fiber = pd.DataFrame({**col_fiber, **{'object': objects}})

        def check_fibers(qtype, qstatus, qarm=None):
            """Fiber query"""
            if qstatus == 'GOOD':
                stat = 1
            elif qstatus == 'BAD':
                stat = 0
            elif qstatus == 'n/a':
                stat = -9999
            else:
                return None

            if qtype == 'STAR':
                qtype = 'STD'

            if qarm == None:
                count = 0
                for i in ['b', 'r', 'z']:
                    obj_statistics = df_fiber.loc[(
                        df_fiber[i] == stat)]['object']
                    count += list(obj_statistics).count(qtype)
                return count
            if qarm in ['b', 'r', 'z']:
                obj_statistics = df_fiber.loc[(
                    df_fiber[qarm] == stat)]['object']
                return list(obj_statistics).count(qtype)
            else:
                return None

        # Fiber classification for ALL arms:
        fiber_class = {}
        for j in ['GOOD', 'BAD', 'n/a']:
            obj_class = {}
            for i in ['TGT', 'STAR']:
                obj_class.update({i: check_fibers(i, j)})
            fiber_class.update({j: obj_class})

        # Fiber classification per EACH arm:
        fiber_class_arm = {}
        for arm in ['b', 'r', 'z']:
            status_class = {}
            for j in ['GOOD', 'BAD', 'n/a']:
                obj_class = {}
                for i in ['TGT', 'STAR']:
                    obj_class.update({i: check_fibers(i, j, qarm=arm)})
                status_class.update({j: obj_class})
            fiber_class_arm.update({arm: status_class})

        # obj_stat= { k: sum([fiber_class[i][k]
        #         for i in ['GOOD', 'BAD']])
        #         for k in ['STAR', 'SKY', 'QSO', 'ELG', 'LRG']}

        return obj_stat_dict, snr_class, fiber_class


if __name__ == '__main__':
    import time
    t1 = time.time()

    # Example:
    # let us say , for instance, we have the following selected exposures:
    exposures_list = [2, 3]

    total_obj = [0]*4
    snr_good = [0]*4
    fib_good = [0]*4
    snr_bad = [0]*4
    fib_bad = [0]*4

    good = [0]*4
    bad = [0]*4

    for iexp in exposures_list:
        nobj, snr, fiber = ObjectStatistics(iexp).generate_statistics()

        print('Nobj:', nobj)
        for i, o in enumerate(['TGT', 'STAR']):
            total_obj[i] += nobj[o]
            good[i] += snr['NORMAL'][o] + snr['WARN'][o] + fiber['GOOD'][o]
            bad[i] += snr['ALARM'][o] + fiber['BAD'][o]

    print('\n\n Statistics:\n\n')
    print('       [TGT, STAR]')
    print('Total  ', total_obj)
    print(' Good  ', [100*good[i]/(good[i] + bad[i]) if (good[i]+bad[i]) > 0
                      else 0 for i in range(4)])
    print('  Bad  ', [100*bad[i]/(good[i] + bad[i]) if (good[i]+bad[i]) > 0
                      else 0 for i in range(4)])

    print(time.time()-t1, ' s')
