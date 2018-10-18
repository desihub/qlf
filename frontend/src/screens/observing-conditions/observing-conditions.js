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

const styles = {
  controlsContainer: {
    display: 'grid',
    alignItems: 'center',
    width: '200px',
    justifyContent: 'space-evenly',
    borderRight: '1px solid darkgrey',
    overflowY: 'auto',
    paddingBottom: '5px',
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
    gridTemplateColumns: 'auto auto',
    height: 'calc(100vh - 135px)',
  },
  viewer: {
    width: 'calc(100vw - 280px)',
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
    paddingBottom: '2.5vh',
  },
  selectionRadio: {
    width: '50%',
    paddingBottom: '2.5vh',
  },
  selectionRadioInner: {
    position: 'relative',
    paddingLeft: '15px',
  },
  formControl: {
    width: '100%',
  },
  button: {
    float: 'right',
    margin: '10px 0',
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
    height: 'calc(100vh - 135px)',
  },
  bulletB: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '7px',
    height: '7px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: 'dodgerblue',
    fontSize: 0,
    textIndent: '-9999em',
    position: 'absolute',
    top: '30px',
    left: '0',
  },
  bulletR: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '7px',
    height: '7px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: 'red',
    fontSize: 0,
    textIndent: '-9999em',
    position: 'absolute',
    top: '78px',
    left: '0',
  },
  bulletZ: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '7px',
    height: '7px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: 'fuchsia',
    fontSize: 0,
    textIndent: '-9999em',
    position: 'absolute',
    top: '126px',
    left: '0',
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
      yaxis: '',
      startDate: '',
      endDate: '',
      datePeriod: '',
      selectYaxis: '',
      selectStartDate: '',
      selectEndDate: '',
      selectArm: '',
      selectSpectrograph: [],
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
        start = moment().format();
        break;
      case 'week':
        start = moment()
          .subtract(7, 'days')
          .format();
        break;
      case 'month':
        start = moment()
          .subtract(1, 'month')
          .format();
        break;
      case 'year':
        start = moment()
          .subtract(1, 'year')
          .format();
        break;
      default:
        return;
    }
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

  handleChangeSpectrograph = spectrograph => {
    this.setState({ spectrograph: [spectrograph], preview: false });
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value, preview: false });
  };

  handleSubmit = () => {
    if (
      this.state.selectYaxis !== this.state.yaxis ||
      this.state.selectStartDate !== this.state.startDate ||
      this.state.selectEndDate !== this.state.endDate ||
      this.state.selectSpectrograph !== this.state.spectrograph ||
      this.state.selectArm !== this.state.arm
    ) {
      this.setState({
        selectYaxis: this.state.yaxis,
        selectStartDate: this.state.startDate,
        selectEndDate: this.state.endDate,
        selectSpectrograph: this.state.spectrograph,
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
    return (
      <div className={this.props.classes.selection}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel shrink>Date Period</InputLabel>
          <Select
            value={this.state.datePeriod}
            onChange={this.handleChangeDatePeriod}
            input={<Input />}
            displayEmpty
            className={this.props.classes.selectEmpty}
          >
            <MenuItem value={'all'}>All</MenuItem>
            <MenuItem value={'night'}>Night</MenuItem>
            <MenuItem value={'week'}>Week</MenuItem>
            <MenuItem value={'month'}>Month</MenuItem>
            <MenuItem value={'year'}>Year</MenuItem>
          </Select>
        </FormControl>
      </div>
    );
  };

  renderYaxisSelection = () => {
    return (
      <div className={this.props.classes.selection}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel shrink>Yaxis</InputLabel>
          <Select
            value={this.state.yaxis}
            onChange={this.handleChangeYaxis}
            input={<Input />}
            displayEmpty
          >
            {/* <MenuItem value={'snr'}>SNR</MenuItem> */}
            <MenuItem value={'skybrightness'}>SKY BRIGHTNESS</MenuItem>
            {/* <MenuItem value={'traceshifts'}>TRACE SHIFTS</MenuItem>
            <MenuItem value={'psf'}>PSF FWHM</MenuItem> */}
            <MenuItem value={'airmass'}>AIRMASS</MenuItem>
          </Select>
        </FormControl>
      </div>
    );
  };

  renderSpectrographSelection = () => {
    return (
      <div className={this.props.classes.SpectroGraph}>
        <InputLabel
          shrink
          className={this.props.classes.spectrographLabel}
          component="legend"
        >
          Spectrograph
        </InputLabel>
        <Petals
          selected={this.state.spectrograph}
          onClick={this.handleChangeSpectrograph}
          size={100}
        />
      </div>
    );
  };

  renderArmSelection = () => {
    return (
      <div className={this.props.classes.selectionRadio}>
        <div className={this.props.classes.selectionRadioInner}>
          <span className={this.props.classes.bulletB}>blue</span>
          <span className={this.props.classes.bulletR}>red</span>
          <span className={this.props.classes.bulletZ}>pink</span>
          <FormControl className={this.props.classes.formControl}>
            <InputLabel shrink>Arm</InputLabel>
            <RadioGroup
              className={this.props.classes.column}
              value={this.state.arm}
              onChange={this.handleChangeArm}
            >
              <FormControlLabel value="b" control={<Radio />} label="b" />
              <FormControlLabel value="r" control={<Radio />} label="r" />
              <FormControlLabel value="z" control={<Radio />} label="z" />
            </RadioGroup>
          </FormControl>
        </div>
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
        {this.renderYaxisSelection()}
        {this.renderSpectrographSelection()}
        {this.renderArmSelection()}
        {this.renderSubmit()}
        {this.renderClear()}
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
          datePeriod={this.state.datePeriod}
          arm={this.state.selectArm}
          spectrograph={this.state.selectSpectrograph}
        />
      );
    }
  };

  render() {
    const { classes } = this.props;
    return (
      <Paper elevation={4} className={classes.main}>
        <div className={classes.gridRow}>
          {this.renderControls()}
          <div className={classes.viewer}>
            {this.renderLoading()}
            {this.renderViewer('timeseries')}
          </div>
        </div>
      </Paper>
    );
  }
}

export default withStyles(styles)(ObservingConditions);
