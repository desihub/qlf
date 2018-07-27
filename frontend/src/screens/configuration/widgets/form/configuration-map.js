export const configMap = [
  {
    label: 'Max Workers',
    helperText: 'Maximum workers running at the same time (0 for unlimited)',
    state: 'maxWorkers',
    api: 'max_workers',
    type: 'workers',
  },
  {
    label: 'Input Directory',
    helperText: 'Input data directory, e.g. full/path/to/spectro/data',
    state: 'input',
    api: 'desi_spectro_data',
    type: 'io',
  },
  {
    label: 'Output Directory',
    helperText:
      'Processing output, e.g. full/path/to/spectro/redux or some other local (fast) scratch area',
    state: 'output',
    api: 'desi_spectro_redux',
    type: 'io',
  },
  {
    label: 'Calibration Directory',
    helperText: 'e.g. full/path/to/spectro/calibration',
    state: 'calibrationPath',
    api: 'calibration_path',
    type: 'io',
  },
  {
    label: 'Warning',
    helperText: '',
    state: 'diskWarning',
    api: 'disk_percent_warning',
    type: 'thresholds',
  },
  {
    label: 'Critical',
    helperText: '',
    state: 'diskAlert',
    api: 'disk_percent_alert',
    type: 'thresholds',
  },
  {
    label: 'Spectrographs',
    helperText: '',
    state: 'spectrographs',
    api: 'spectrographs',
    type: 'pipeline',
  },
  {
    label: 'Arms',
    helperText: '',
    state: 'arms',
    api: 'arms',
    type: 'pipeline',
  },
];
