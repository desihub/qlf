import yaml


def get_plot_data():

    stream = open('test/data/qa-snr-r0-00000000.yaml', 'r')

    data = yaml.load(stream)

    elg_mag = data['SNR']['VALUE']['ELG_SNR_MAG'][1]
    elg_snr = data['SNR']['VALUE']['ELG_SNR_MAG'][0]
    elg_fiber_id = data['SNR']['VALUE']['ELG_FIBERID']

    lrg_mag = data['SNR']['VALUE']['LRG_SNR_MAG'][1]
    lrg_snr = data['SNR']['VALUE']['LRG_SNR_MAG'][0]
    lrg_fiber_id = data['SNR']['VALUE']['LRG_FIBERID']

    qso_mag = data['SNR']['VALUE']['QSO_SNR_MAG'][1]
    qso_snr = data['SNR']['VALUE']['QSO_SNR_MAG'][0]
    qso_fiber_id = data['SNR']['VALUE']['QSO_FIBERID']

    star_mag = data['SNR']['VALUE']['STAR_SNR_MAG'][1]
    star_snr = data['SNR']['VALUE']['STAR_SNR_MAG'][0]
    star_fiber_id = data['SNR']['VALUE']['STAR_FIBERID']

    return {'elg_mag': elg_mag,
            'elg_snr': elg_snr,
            'elg_fiber_id': elg_fiber_id,
            'lrg_mag': lrg_mag,
            'lrg_snr': lrg_snr,
            'lrg_fiber_id': lrg_fiber_id,
            'qso_mag': qso_mag,
            'qso_snr': qso_snr,
            'qso_fiber_id': qso_fiber_id,
            'star_mag': star_mag,
            'star_snr': star_snr,
            'star_fiber_id': star_fiber_id}
