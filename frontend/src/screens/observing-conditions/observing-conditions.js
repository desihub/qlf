import React from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import { FadeLoader } from 'halogenium';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import ObservingViewer from './observing-viewer/observing-viewer';
import SelectDate from '../../components/select-date/select-date';
import moment from 'moment';
import Petals from '../../components/petals/petals';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Radio from '@material-ui/core/Radio';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import LegendDate from '../../components/legend-date/legend-date';
import Checkbox from '@material-ui/core/Checkbox';
import FormGroup from '@material-ui/core/FormGroup';

const styles = {
  controlsContainer: {
    width: '12vw',
    borderRight: '1px solid darkgrey',
    overflow: 'auto',
    paddingRight: '10px',
    boxSizing: 'border-box',
  },
  controlsContainerInner: {
    display: 'flex',
    flexDirection: 'row',
  },
  column: {
    display: 'flex',
    flexDirection: 'column',
    paddingTop: '10px',
  },
  gridRow: {
    display: 'grid',
    gridTemplateColumns: '12vw calc(100vw - 64px - 12vw)',
    width: 'calc(100vw - 64px)',
    height: 'calc(100vh - 127px - 1.2vw - 4.8vh)',
  },
  viewer: {
    width: 'calc(100vw - 64px - 12vw)',
  },
  fadeLoaderFull: {
    position: 'absolute',
    paddingLeft: 'calc((100vw - 40px) / 2)',
    paddingTop: 'calc(25vh)',
  },
  fadeLoader: {
    position: 'absolute',
    paddingLeft: 'calc((100vw - 300px) / 2)',
    paddingTop: 'calc(25vh)',
  },
  selection: {
    textAlign: 'center',
    position: 'relative',
  },
  selectionRadio: {
    width: '50%',
  },
  formControl: {
    width: '100%',
  },
  buttons: {
    display: 'grid',
  },
  button: {
    float: 'right',
    margin: '10px 0',
    fontSize: '1vw',
  },
  buttonGreen: {
    backgroundColor: 'green',
    color: 'white',
  },
  SpectroGraph: {
    paddingBottom: '2.5vh',
    textAlign: 'center',
  },
  spectrographLabel: {
    paddingBottom: 10,
    textAlign: 'left',
  },
  main: {
    margin: '16px',
    padding: '16px',
    height: 'calc(100vh - 130px)',
  },
  title: {
    fontSize: '1.2vw',
    textAlign: 'left',
  },
  text: {
    fontSize: '1vw',
  },
  tabItem: {
    fontSize: '1.2vw',
  },
  tabsH: {
    minHeight: '4.8vh',
    marginBottom: '20px',
  },
  tabWH: {
    minWidth: '11vw',
    minHeight: '4.8vh',
  },
  selectEmpty: {
    fontSize: '1vw',
    marginTop: '1vh',
    lineHeight: '2.5vh',
  },
  radioGroup: {
    fontSize: '1vw',
    marginTop: '2vh',
  },
  lineH: {
    height: '4.87vh',
    marginLeft: 0,
  },
  wh: {
    width: '1.7vw',
    height: '3.5vh',
  },
  selectIcon: {
    width: '1.7vw',
    height: '3.5vh',
    top: 'calc(50% - 1.6vh)',
  },
  textLabel: {
    fontSize: '1vw',
    marginLeft: '0.5vw',
  },
  mItem: {
    height: '2.4vh',
    fontSize: '1vw',
  },
  space: {
    position: 'relative',
  },
};

class ObservingConditions extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      firstLoad: false,
      spectrograph: [],
      arm: '',
      xaxis: '',
      yaxis: '',
      startDate: '',
      endDate: '',
      datePeriod: 'all',
      selectYaxis: '',
      selectXaxis: '',
      selectStartDate: '',
      selectEndDate: '',
      selectArm: '',
      selectSpectrograph: [],
      tab: 'Time Series',
      selectDatashader: '',
      datashader: false,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    startDate: PropTypes.string.isRequired,
    endDate: PropTypes.string.isRequired,
  };

  componentDidMount() {
    document.title = 'Observing Conditions';
  }

  componentWillReceiveProps(nextProps) {
    if (this.state.startDate === '' && this.state.endDate === '')
      this.setState({
        startDate: nextProps.startDate,
        endDate: nextProps.endDate,
      });
  }

  handleChangeDatashader = () => {
    this.setState({ datashader: !this.state.datashader, preview: false });
  };

  handleChangeDatePeriod = evt => {
    let start = null;
    switch (evt.target.value) {
      case 'all':
        this.setState({
          datePeriod: evt.target.value,
          startDate: this.props.startDate,
          endDate: this.props.endDate,
          preview: false,
        });
        return;
      case 'night':
        start = moment();
        break;
      case 'week':
        start = moment().subtract(7, 'days');
        break;
      case 'month':
        start = moment().subtract(1, 'month');
        break;
      case 'year':
        start = moment().subtract(1, 'year');
        break;
      default:
        return;
    }
    const firstDate = moment(this.props.startDate);
    start = moment(start).diff(firstDate) > 0 ? start : firstDate;
    this.setState({
      datePeriod: evt.target.value,
      startDate: moment(start).format('YYYY-MM-DD'),
      endDate: moment().format('YYYY-MM-DD'),
      preview: false,
    });
  };

  handleChangeYaxis = evt => {
    this.setState({ yaxis: evt.target.value, preview: false });
  };

  handleChangeXaxis = evt => {
    this.setState({ xaxis: evt.target.value, preview: false });
  };

  handleChangeSpectrograph = spectrograph => {
    this.setState({ spectrograph: [spectrograph], preview: false });
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value, preview: false });
  };

  handleSubmit = () => {
    if (
      this.state.selectYaxis !== this.state.yaxis ||
      this.state.selectXaxis !== this.state.xaxis ||
      this.state.selectStartDate !== this.state.startDate ||
      this.state.selectEndDate !== this.state.endDate ||
      this.state.selectSpectrograph !== this.state.spectrograph ||
      this.state.selectDatashader !== this.state.datashader ||
      this.state.selectArm !== this.state.arm
    ) {
      this.setState({
        selectXaxis: this.state.xaxis,
        selectYaxis: this.state.yaxis,
        selectStartDate: this.state.startDate,
        selectEndDate: this.state.endDate,
        selectSpectrograph: this.state.spectrograph,
        selectDatashader: this.state.datashader,
        selectArm: this.state.arm,
      });
      this.loadStart();
    }
  };

  loadStart = () => {
    this.setState({ loading: true, preview: true });
  };

  loadEnd = () => {
    this.setState({ loading: false });
  };

  renderLoading = () => {
    if (!this.state.loading) return null;
    const showControls =
      this.state.yaxis ||
      this.state.startDate ||
      this.state.endDate ||
      this.state.arm ||
      this.state.spectrograph;
    const classLoading = showControls
      ? styles.fadeLoader
      : styles.fadeLoaderFull;

    if (
      this.state.yaxis !== '' &&
      this.state.startDate !== '' &&
      this.state.endDate !== '' &&
      this.state.arm !== '' &&
      this.state.spectrograph.length !== 0
    ) {
      return (
        <div className={this.props.classes.loading}>
          <FadeLoader
            style={classLoading}
            color="#424242"
            size="16px"
            margin="4px"
          />
        </div>
      );
    }
  };

  isValid = () => {
    return (
      this.state.yaxis !== '' &&
      this.state.startDate !== '' &&
      this.state.endDate !== '' &&
      this.state.arm !== '' &&
      this.state.spectrograph.length !== 0
    );
  };

  clearSelection = () => {
    this.setState({
      yaxis: '',
      loading: false,
      datePeriod: '',
      preview: false,
      arm: '',
      spectrograph: [],
    });
  };

  renderDatePeriodSelection = () => {
    const { classes } = this.props;
    return (
      <div className={this.props.classes.selection}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel
            shrink
            style={styles.space}
            classes={{ root: classes.title }}
          >
            Date Period
          </InputLabel>
          <LegendDate />
          <Select
            value={this.state.datePeriod}
            onChange={this.handleChangeDatePeriod}
            input={<Input />}
            displayEmpty
            classes={{ root: classes.selectEmpty, icon: classes.selectIcon }}
          >
            <MenuItem value={'all'} classes={{ root: classes.mItem }}>
              All
            </MenuItem>
            <MenuItem value={'night'} classes={{ root: classes.mItem }}>
              Night
            </MenuItem>
            <MenuItem value={'week'} classes={{ root: classes.mItem }}>
              Week
            </MenuItem>
            <MenuItem value={'month'} classes={{ root: classes.mItem }}>
              Month
            </MenuItem>
            <MenuItem value={'year'} classes={{ root: classes.mItem }}>
              Year
            </MenuItem>
          </Select>
        </FormControl>
      </div>
    );
  };

  renderXaxisSelection = () => {
    const { classes } = this.props;
    if (this.state.tab !== 'Time Series')
      return (
        <div className={this.props.classes.selection}>
          <FormControl className={this.props.classes.formControl}>
            <InputLabel shrink classes={{ root: classes.title }}>
              Xaxis
            </InputLabel>
            <Select
              value={this.state.xaxis}
              onChange={this.handleChangeXaxis}
              input={<Input />}
              displayEmpty
              classes={{ root: classes.selectEmpty, icon: classes.selectIcon }}
            >
              {/* <MenuItem value={'snr'} classes={{ root: classes.mItem }}>
                SNR
              </MenuItem> */}
              <MenuItem
                value={'skybrightness'}
                classes={{ root: classes.mItem }}
              >
                SKY BRIGHTNESS
              </MenuItem>
              {/* <MenuItem value={'traceshifts'} classes={{ root: classes.mItem }}>
                TRACE SHIFTS
              </MenuItem>
              <MenuItem value={'psf'} classes={{ root: classes.mItem }}>
                PSF FWHM
              </MenuItem> */}
              <MenuItem value={'airmass'} classes={{ root: classes.mItem }}>
                AIRMASS
              </MenuItem>
            </Select>
          </FormControl>
        </div>
      );
  };

  renderYaxisSelection = () => {
    const { classes } = this.props;
    return (
      <div className={this.props.classes.selection}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel shrink classes={{ root: classes.title }}>
            Yaxis
          </InputLabel>
          <Select
            value={this.state.yaxis}
            onChange={this.handleChangeYaxis}
            input={<Input />}
            displayEmpty
            classes={{ root: classes.selectEmpty, icon: classes.selectIcon }}
          >
            {/* <MenuItem value={'snr'} classes={{ root: classes.mItem }}>
              SNR
            </MenuItem> */}
            <MenuItem value={'skybrightness'} classes={{ root: classes.mItem }}>
              SKY BRIGHTNESS
            </MenuItem>
            {/* <MenuItem value={'traceshifts'} classes={{ root: classes.mItem }}>
              TRACE SHIFTS
            </MenuItem>
            <MenuItem value={'psf'}>PSF FWHM</MenuItem> */}
            <MenuItem value={'airmass'} classes={{ root: classes.mItem }}>
              AIRMASS
            </MenuItem>
          </Select>
        </FormControl>
      </div>
    );
  };

  renderSpectrographSelection = () => {
    const { classes } = this.props;
    return (
      <div className={this.props.classes.SpectroGraph}>
        <InputLabel
          shrink
          className={this.props.classes.spectrographLabel}
          component="legend"
          classes={{ root: classes.title }}
        >
          Spectrograph
        </InputLabel>
        <Petals
          selected={this.state.spectrograph}
          onClick={this.handleChangeSpectrograph}
          size={22}
        />
      </div>
    );
  };

  renderArmSelection = () => {
    const { classes } = this.props;
    return (
      <div className={this.props.classes.selectionRadio}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel shrink classes={{ root: classes.title }}>
            Arm
          </InputLabel>
          <RadioGroup
            className={this.props.classes.column}
            value={this.state.arm}
            onChange={this.handleChangeArm}
            classes={{ root: classes.radioGroup }}
          >
            <FormControlLabel
              value="b"
              control={<Radio classes={{ root: classes.wh }} />}
              label="b"
              classes={{ label: classes.textLabel, root: classes.lineH }}
            />
            <FormControlLabel
              value="r"
              control={<Radio classes={{ root: classes.wh }} />}
              label="r"
              classes={{ label: classes.textLabel, root: classes.lineH }}
            />
            <FormControlLabel
              value="z"
              control={<Radio classes={{ root: classes.wh }} />}
              label="z"
              classes={{ label: classes.textLabel, root: classes.lineH }}
            />
          </RadioGroup>
        </FormControl>
      </div>
    );
  };

  renderClear = () => (
    <Button
      onClick={this.clearSelection}
      variant="raised"
      size="small"
      className={this.props.classes.button}
      disabled={!this.isValid()}
    >
      Clear
    </Button>
  );

  renderSubmit = () => (
    <Button
      onClick={this.handleSubmit}
      variant="raised"
      size="small"
      className={this.props.classes.button}
      classes={{ raised: this.props.classes.buttonGreen }}
      disabled={!this.isValid()}
    >
      Submit
    </Button>
  );

  renderDatashadeSelection = () => {
    const { classes } = this.props;
    if (this.state.tab === 'Time Series') {
      return (
        <div className={this.props.classes.selectionRadio}>
          <FormControl className={this.props.classes.formControl}>
            <FormGroup className={this.props.classes.column}>
              <FormControlLabel
                value={this.state.datashader}
                control={
                  <Checkbox
                    checked={this.state.datashader}
                    onChange={this.handleChangeDatashader}
                    classes={{ root: classes.wh }}
                  />
                }
                label={'Datashader'}
                classes={{ label: classes.text, root: classes.lineH }}
              />
            </FormGroup>
          </FormControl>
        </div>
      );
    }
  };

  renderSelectDate = () => {
    if (this.state.startDate !== '' && this.state.endDate !== '')
      return (
        <SelectDate
          startDate={this.state.startDate}
          endDate={this.state.endDate}
          setHistoryRangeDate={this.setHistoryRangeDate}
        />
      );
  };

  setHistoryRangeDate = (startDate, endDate) => {
    this.setState({
      datePeriod: '',
      startDate,
      endDate,
    });
  };

  renderControls = () => {
    const { classes } = this.props;
    return (
      <div className={classes.controlsContainer}>
        {this.renderDatePeriodSelection()}
        {this.renderSelectDate()}
        {this.renderXaxisSelection()}
        {this.renderYaxisSelection()}
        {this.renderSpectrographSelection()}
        {this.renderArmSelection()}
        {this.renderDatashadeSelection()}
        <div className={classes.buttons}>
          {this.renderSubmit()}
          {this.renderClear()}
        </div>
      </div>
    );
  };

  renderViewer = plot => {
    if (this.state.preview) {
      return (
        <ObservingViewer
          plot={plot}
          loadEnd={this.loadEnd}
          startDate={this.state.selectStartDate}
          endDate={this.state.selectEndDate}
          yaxis={this.state.selectYaxis}
          xaxis={this.state.selectXaxis}
          datashader={this.state.selectDatashader}
          datePeriod={this.state.datePeriod}
          arm={this.state.selectArm}
          spectrograph={this.state.selectSpectrograph}
        />
      );
    }
  };

  renderTimeSeries = () => {
    const { classes } = this.props;
    return (
      <div className={classes.gridRow}>
        {this.renderControls()}
        <div className={classes.viewer}>
          {this.renderLoading()}
          {this.renderViewer('timeseries')}
        </div>
      </div>
    );
  };

  renderRegression = () => {
    const { classes } = this.props;
    return (
      <div className={classes.gridRow}>
        {this.renderControls()}
        <div className={classes.viewer}>
          {this.renderLoading()}
          {this.renderViewer('regression')}
        </div>
      </div>
    );
  };

  handleTabChange = (evt, tab) => {
    this.setState({ tab });
    this.clearSelection();
  };

  renderTabs = () => {
    const { tab } = this.state;
    const { classes } = this.props;
    return (
      <div>
        <Tabs
          value={tab}
          onChange={this.handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
          style={styles.tabsH}
        >
          <Tab
            label="Time Series"
            value={'Time Series'}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="Regression"
            value={'Regression'}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
        </Tabs>
        {tab === 'Time Series' ? this.renderTimeSeries() : null}
        {tab === 'Regression' ? this.renderRegression() : null}
      </div>
    );
  };

  render() {
    const { classes } = this.props;
    return (
      <Paper elevation={4} className={classes.main}>
        {this.renderTabs()}
      </Paper>
    );
  }
}

export default withStyles(styles)(ObservingConditions);
