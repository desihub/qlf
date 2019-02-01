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
import LegendDate from '../../components/legend-date/legend-date';

const styles = {
  controlsContainer: {
    width: '12vw',
    borderRight: '1px solid darkgrey',
    overflowY: 'auto',
    paddingRight: '10px',
    boxSizing: 'border-box',
  },
  column: {
    display: 'flex',
    flexDirection: 'column',
  },
  gridRow: {
    display: 'grid',
    gridTemplateColumns: '12vw calc(100vw - 64px - 12vw)',
    width: 'calc(100vw - 64px)',
    height: 'calc(100vh - 135px)',
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
    paddingBottom: '2.5vh',
  },
  formControl: {
    width: '100%',
  },
  buttons: {
    display: 'grid',
    width: '10vw',
    alignItems: 'center',
    height: '13vh',
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
  spectrographLabel: {
    paddingBottom: 10,
  },
  main: {
    margin: '16px',
    padding: '16px',
    height: 'calc(100vh - 135px)',
  },
  title: {
    fontSize: '1.2vw',
    textAlign: 'left',
  },
  text: {
    fontSize: '1.1vw',
  },
  selectEmpty: {
    fontSize: '1vw',
    marginTop: '1vh',
    lineHeight: '2.5vh',
  },
  selectIcon: {
    width: '1.7vw',
    height: '3.5vh',
    top: 'calc(50% - 1.6vh)',
  },
  mItem: {
    height: '2.4vh',
    fontSize: '1vw',
  },
  space: {
    position: 'relative',
  },
};

class SurveyReport extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      datePeriod: 'all',
      startDate: '',
      endDate: '',
      program: '',
      loading: false,
      firstLoad: false,
      selectProgram: '',
      selectStartDate: '',
      selectEndDate: '',
      preview: true,
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
    if (evt.target.value !== this.state.program)
      this.setState({ program: evt.target.value, preview: false });
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
    if (evt.target.value !== this.state.datePeriod)
      this.setState({
        datePeriod: evt.target.value,
        startDate: moment(start).format('YYYY-MM-DD'),
        endDate: moment().format('YYYY-MM-DD'),
        preview: false,
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
      preview: false,
    });
  };

  renderProgramSelection = () => {
    const { classes } = this.props;
    return (
      <div className={this.props.classes.selection}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel shrink classes={{ root: classes.title }}>
            Program
          </InputLabel>
          <Select
            value={this.state.program}
            onChange={this.handleChangeProgram}
            input={<Input />}
            displayEmpty
            classes={{ root: classes.selectEmpty, icon: classes.selectIcon }}
          >
            <MenuItem value={'all'} classes={{ root: classes.mItem }}>
              All
            </MenuItem>
            <MenuItem value={'bright'} classes={{ root: classes.mItem }}>
              Bright
            </MenuItem>
            <MenuItem value={'dark'} classes={{ root: classes.mItem }}>
              Dark
            </MenuItem>
            <MenuItem value={'gray'} classes={{ root: classes.mItem }}>
              Gray
            </MenuItem>
          </Select>
        </FormControl>
      </div>
    );
  };

  renderControls = () => {
    const { classes } = this.props;
    return (
      <div className={classes.controlsContainer}>
        {this.renderProgramSelection()}
        {this.renderDatePeriodSelection()}
        {this.renderSelectDate()}
        <div className={classes.buttons}>
          {this.renderSubmit()}
          {this.renderClear()}
        </div>
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
