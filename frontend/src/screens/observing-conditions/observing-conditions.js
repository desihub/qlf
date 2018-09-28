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
    height: 'calc(100vh - 200px)',
    paddingTop: '16px',
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
  formControl: {
    width: '100%',
  },
  button: {
    float: 'right',
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
};

class TrendAnalysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      firstLoad: false,
      yaxis: '',
      startDate: '',
      endDate: '',
      datePeriod: '',
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    startDate: PropTypes.string.isRequired,
    endDate: PropTypes.string.isRequired,
  };

  componentWillReceiveProps(nextProps) {
    if (this.state.startDate === '' && this.state.endDate === '')
      this.setState({
        startDate: nextProps.startDate,
        endDate: nextProps.endDate,
      });
  }

  handleChangeDatePeriod = evt => {
    this.setState({ datePeriod: evt.target.value, endDate: moment().format() });
    this.loadStart();
    switch (evt.target.value) {
      case 'night':
        this.setState({ startDate: moment().format() });
        break;
      case 'week':
        this.setState({
          startDate: moment()
            .subtract(7, 'days')
            .format(),
        });
        break;
      case 'month':
        this.setState({
          startDate: moment()
            .subtract(1, 'month')
            .format(),
        });
        break;
      case 'semester':
        this.setState({
          startDate: moment()
            .subtract(6, 'month')
            .format(),
        });
        break;
      case 'year':
        this.setState({
          startDate: moment()
            .subtract(1, 'year')
            .format(),
        });
        break;
      default:
        return;
    }
  };

  handleChangeYaxis = evt => {
    this.setState({ yaxis: evt.target.value });
    this.loadStart();
  };

  loadStart = () => {
    this.setState({ loading: true });
  };

  loadEnd = () => {
    this.setState({ loading: false });
  };

  renderLoading = () => {
    if (!this.state.loading) return null;
    const showControls = this.state.datePeriod || this.state.yaxis;
    const classLoading = showControls
      ? styles.fadeLoader
      : styles.fadeLoaderFull;

    if (this.state.yaxis !== '' && this.state.datePeriod !== '') {
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

  clearSelection = () => {
    this.setState({
      yaxis: '',
      loading: false,
      datePeriod: '',
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
            <MenuItem value={'night'}>Night</MenuItem>
            <MenuItem value={'week'}>Week</MenuItem>
            <MenuItem value={'month'}>Month</MenuItem>
            <MenuItem value={'semester'}>Semester</MenuItem>
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
            <MenuItem value={'snr'}>SNR</MenuItem>
            <MenuItem value={'skybrightness'}>SKY BRIGHTNESS</MenuItem>
            <MenuItem value={'traceshifts'}>TRACE SHIFTS</MenuItem>
            <MenuItem value={'psffwhm'}>PSF FWHM</MenuItem>
            <MenuItem value={'airmass'}>AIRMASS</MenuItem>
          </Select>
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
    >
      Clear
    </Button>
  );

  renderSelectDate = () => {
    if (this.props.startDate !== '' && this.props.endDate !== '')
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
        {this.renderClear()}
      </div>
    );
  };

  renderViewer = plot => {
    return (
      <ObservingViewer
        plot={plot}
        loadEnd={this.loadEnd}
        startDate={this.state.startDate}
        endDate={this.state.endDate}
        yaxis={this.state.yaxis}
        datePeriod={this.state.datePeriod}
      />
    );
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

export default withStyles(styles)(TrendAnalysis);
