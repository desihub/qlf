export const processColumns = [
  {
    key: 'runtime',
    name: 'Status',
    type: 'status',
  },
  {
    key: 'exposure__program',
    name: 'Program',
    type: 'normal',
  },
  {
    key: 'pk',
    name: 'Process ID',
    type: 'parent',
  },
  {
    key: 'exposure_id',
    name: 'Exp ID',
    type: 'normal',
  },
  {
    key: 'exposure__flavor',
    name: 'Flavor',
    type: 'normal',
  },
  {
    key: 'exposure__tile',
    name: 'Tile ID',
    type: 'normal',
  },
  {
    key: 'start',
    name: 'Process Date',
    type: 'dateprocess',
  },
  {
    key: 'runtime',
    name: 'Process Time',
    type: 'runtime',
  },
  {
    key: 'exposure__dateobs',
    name: 'OBS Date',
    type: 'date',
  },
  {
    key: '',
    name: 'MJD',
    type: 'datemjd',
  },
  {
    key: 'exposure__telra',
    name: 'RA (hms)',
    type: 'normal',
  },
  {
    key: 'exposure__teldec',
    name: 'Dec (dms)',
    type: 'normal',
  },
  {
    key: 'exposure__exptime',
    name: 'Exp Time(s)',
    type: 'normal',
  },
  {
    key: 'exposure__airmass',
    name: 'Airmass',
    type: 'normal',
  },
  {
    key: '',
    name: 'FWHM (arcsec)',
    type: null,
  },
  {
    key: '',
    name: 'QA',
    type: 'qa',
  },
  {
    key: '',
    name: 'CCDs',
    type: 'image',
  },
  {
    key: '',
    name: 'COM',
    type: 'comments',
  },
];
