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
import SurveyViewer from './survey-viewer/survey-viewer';
import SelectDate from '../../components/select-date/select-date';
import moment from 'moment';

const styles = {
  controlsContainer: {
    display: 'grid',
    alignItems: 'center',
    width: 200,
    justifyContent: 'space-evenly',
    borderRight: '1px solid darkgrey',
    overflowY: 'auto',
  },
  column: {
    display: 'flex',
    flexDirection: 'column',
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
  spectrographLabel: {
    paddingBottom: 10,
  },
  main: {
    margin: '16px',
    padding: '16px',
    height: 'calc(100vh - 135px)',
  },
};

class SurveyReport extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      datePeriod: '',
      startDate: '',
      endDate: '',
      program: '',
      loading: false,
      firstLoad: false,
      selectProgram: '',
      selectStartDate: '',
      selectEndDate: '',
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    startDate: PropTypes.string.isRequired,
    endDate: PropTypes.string.isRequired,
  };

  componentDidMount() {
    document.title = 'Survey Report';
  }

  componentWillReceiveProps(nextProps) {
    if (this.state.startDate === '' && this.state.endDate === '')
      this.setState({
        startDate: nextProps.startDate,
        endDate: nextProps.endDate,
      });
  }

  handleChangeProgram = evt => {
    this.setState({ program: evt.target.value });
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
      case 'semester':
        start = moment()
          .subtract(6, 'month')
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
    });
  };

  handleSubmit = () => {
    if (
      this.state.selectProgram !== this.state.program ||
      this.state.selectStartDate !== this.state.startDate ||
      this.state.selectEndDate !== this.state.endDate
    ) {
      this.setState({
        selectProgram: this.state.program,
        selectStartDate: this.state.startDate,
        selectEndDate: this.state.endDate,
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
      this.state.startDate || this.state.endDate || this.state.program;
    const classLoading = showControls
      ? styles.fadeLoader
      : styles.fadeLoaderFull;

    if (
      this.state.startDate !== '' &&
      this.state.endDate !== '' &&
      this.state.program !== ''
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
      this.state.program !== '' &&
      this.state.startDate !== '' &&
      this.state.endDate !== ''
    );
  };

  clearSelection = () => {
    this.setState({
      datePeriod: '',
      program: '',
      loading: false,
      preview: false,
    });
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

  renderProgramSelection = () => {
    return (
      <div className={this.props.classes.selection}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel shrink>Program</InputLabel>
          <Select
            value={this.state.program}
            onChange={this.handleChangeProgram}
            input={<Input />}
            displayEmpty
            className={this.props.classes.selectEmpty}
          >
            <MenuItem value={'all'}>All</MenuItem>
            <MenuItem value={'bright'}>Bright</MenuItem>
            <MenuItem value={'dark'}>Dark</MenuItem>
            <MenuItem value={'gray'}>Gray</MenuItem>
          </Select>
        </FormControl>
      </div>
    );
  };

  renderControls = () => {
    const { classes } = this.props;
    return (
      <div className={classes.controlsContainer}>
        {this.renderDatePeriodSelection()}
        {this.renderSelectDate()}
        {this.renderProgramSelection()}
        {this.renderSubmit()}
        {this.renderClear()}
      </div>
    );
  };

  renderViewer = () => {
    if (this.state.preview) {
      return (
        <SurveyViewer
          datePeriod={this.state.datePeriod}
          startDate={this.state.selectStartDate}
          endDate={this.state.selectEndDate}
          program={this.state.selectProgram}
          loadEnd={this.loadEnd}
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
            {this.renderViewer()}
          </div>
        </div>
      </Paper>
    );
  }
}

export default withStyles(styles)(SurveyReport);
