import React from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';
import FormGroup from '@material-ui/core/FormGroup';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import { FadeLoader } from 'halogenium';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import TrendViewer from './trend-viewer/trend-viewer';
import SelectDate from '../../components/select-date/select-date';
import Petals from '../../components/petals/petals';
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
    paddingBottom: '2.5vh',
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
    height: 'calc(100vh - 135px)',
  },
  title: {
    fontSize: '1.2vw',
    textAlign: 'left',
  },
  text: {
    fontSize: '1vw',
    marginLeft: '0.5vw',
  },
  selectEmpty: {
    fontSize: '1vw',
    marginTop: '1vh',
    lineHeight: '2.5vh',
  },
  radioGroup: {
    fontSize: '1vw',
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
  mItem: {
    height: '2.4vh',
    fontSize: '1vw',
  },
  space: {
    position: 'relative',
  },
};

class TrendAnalysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tab: 'Time Series',
      spectrograph: [],
      arm: '',
      amp: [],
      loading: false,
      firstLoad: false,
      xaxis: '',
      yaxis: '',
      startDate: '',
      endDate: '',
      datePeriod: 'all',
      selectArm: '',
      selectAmp: [],
      selectXaxis: '',
      selectYaxis: '',
      selectStartDate: '',
      selectEndDate: '',
      selectSpectrograph: [],
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
    document.title = 'Trend Analysis';
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

  handleChangeDatashader = () => {
    this.setState({ datashader: !this.state.datashader, preview: false });
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value, preview: false });
  };

  handleChangeAmp = value => () => {
    if (value === 'all') {
      this.state.amp.includes(value)
        ? this.setState({ amp: [], preview: false })
        : this.setState({ amp: ['all', '1', '2', '3', '4'], preview: false });
    } else {
      const amps = this.state.amp.includes(value)
        ? this.state.amp.filter(v => v !== value)
        : this.state.amp.concat(value);
      this.setState({ amp: amps, preview: false });
    }
  };

  handleChangeXaxis = evt => {
    this.setState({ xaxis: evt.target.value, preview: false });
  };

  handleChangeYaxis = evt => {
    this.setState({ yaxis: evt.target.value, preview: false });
  };

  handleChangeSpectrograph = spectrograph => {
    this.setState({ spectrograph: [spectrograph], preview: false });
  };

  handleSubmit = () => {
    if (
      this.state.selectArm !== this.state.arm ||
      this.state.selectAmp.length !== this.state.amp.length ||
      this.state.selectAmp[0] !== this.state.amp[0] ||
      this.state.selectXaxis !== this.state.xaxis ||
      this.state.selectYaxis !== this.state.yaxis ||
      this.state.selectSpectrograph.length !== this.state.spectrograph.length ||
      this.state.selectSpectrograph[0] !== this.state.spectrograph[0] ||
      this.state.selectDatashader !== this.state.datashader ||
      this.state.selectStartDate !== this.state.startDate ||
      this.state.selectEndDate !== this.state.endDate
    ) {
      this.setState({
        selectArm: this.state.arm,
        selectAmp: this.state.amp,
        selectXaxis: this.state.xaxis,
        selectYaxis: this.state.yaxis,
        selectDatashader: this.state.datashader,
        selectSpectrograph: this.state.spectrograph,
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
      this.state.startDate ||
      this.state.endDate ||
      this.state.arm ||
      this.state.amp ||
      this.state.spectrograph ||
      this.state.xaxis ||
      this.state.yaxis;
    const classLoading = showControls
      ? styles.fadeLoader
      : styles.fadeLoaderFull;

    if (
      (this.state.tab === 'Time Series' &&
        this.state.amp.length !== 0 &&
        this.state.arm !== '' &&
        this.state.yaxis !== '' &&
        this.state.startDate !== '' &&
        this.state.endDate !== '' &&
        this.state.spectrograph.length !== 0) ||
      (this.state.tab === 'Regression' &&
        this.state.amp.length !== 0 &&
        this.state.arm !== '' &&
        this.state.yaxis !== '' &&
        this.state.xaxis !== '' &&
        this.state.startDate !== '' &&
        this.state.endDate !== '' &&
        this.state.spectrograph.length !== 0)
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
    if (this.state.tab === 'Time Series') {
      return (
        this.state.amp.length !== 0 &&
        this.state.arm !== '' &&
        this.state.yaxis !== '' &&
        this.state.startDate !== '' &&
        this.state.endDate !== '' &&
        this.state.spectrograph.length !== 0
      );
    }

    if (this.state.tab === 'Regression') {
      return (
        this.state.amp.length !== 0 &&
        this.state.arm !== '' &&
        this.state.yaxis !== '' &&
        this.state.xaxis !== '' &&
        this.state.startDate !== '' &&
        this.state.endDate !== '' &&
        this.state.spectrograph.length !== 0
      );
    }
  };

  clearSelection = () => {
    this.setState({
      arm: '',
      amp: '',
      xaxis: '',
      yaxis: '',
      loading: false,
      spectrograph: [],
      datePeriod: '',
      preview: false,
    });
  };

  renderDatePeriodSelection = () => {
    const { classes } = this.props;
    return (
      <div className={classes.selection}>
        <FormControl className={classes.formControl}>
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

  renderYaxisSelection = () => {
    const { classes } = this.props;
    return (
      <div className={classes.selection}>
        <FormControl className={classes.formControl}>
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
            <MenuItem value={'noise'} classes={{ root: classes.mItem }}>
              Noise
            </MenuItem>
            <MenuItem value={'bias'} classes={{ root: classes.mItem }}>
              Bias
            </MenuItem>
          </Select>
        </FormControl>
      </div>
    );
  };

  renderAmpSelection = () => {
    const { classes } = this.props;
    return (
      <div className={this.props.classes.selectionRadio}>
        <FormControl className={this.props.classes.formControl}>
          <InputLabel shrink classes={{ root: classes.title }}>
            Amp
          </InputLabel>
          <FormGroup className={this.props.classes.column}>
            {['all', '1', '2', '3', '4'].map(val => {
              return (
                <FormControlLabel
                  key={val}
                  value={val}
                  control={
                    <Checkbox
                      checked={this.state.amp.includes(val)}
                      onChange={this.handleChangeAmp(val)}
                      classes={{ root: classes.wh }}
                    />
                  }
                  label={val}
                  classes={{ label: classes.text, root: classes.lineH }}
                />
              );
            })}
          </FormGroup>
        </FormControl>
      </div>
    );
  };

  renderDatashadeSelection = () => {
    const { classes } = this.props;
    return (
      <div className={this.props.classes.selectionRadio}>
        <FormControl className={this.props.classes.formControl}>
          <FormGroup className={this.props.classes.column}>
            <FormControlLabel
              value={String(this.state.datashader)}
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
  };

  renderArmSelection = () => {
    const { classes } = this.props;
    return (
      <div className={classes.selectionRadio}>
        <FormControl className={classes.formControl}>
          <InputLabel shrink classes={{ root: classes.title }}>
            Arm
          </InputLabel>
          <RadioGroup
            className={classes.column}
            value={this.state.arm}
            onChange={this.handleChangeArm}
            classes={{ root: classes.radioGroup }}
          >
            <FormControlLabel
              value="b"
              control={<Radio classes={{ root: classes.wh }} />}
              label="b"
              classes={{ label: classes.text, root: classes.lineH }}
            />
            <FormControlLabel
              value="r"
              control={<Radio classes={{ root: classes.wh }} />}
              label="r"
              classes={{ label: classes.text, root: classes.lineH }}
            />
            <FormControlLabel
              value="z"
              control={<Radio classes={{ root: classes.wh }} />}
              label="z"
              classes={{ label: classes.text, root: classes.lineH }}
            />
          </RadioGroup>
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
        {this.renderYaxisSelection()}
        {this.renderSpectrographSelection()}
        <div className={classes.controlsContainerInner}>
          {this.renderAmpSelection()}
          {this.renderArmSelection()}
        </div>
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
        <TrendViewer
          plot={plot}
          amp={this.state.amp.filter(v => v !== 'all')}
          arm={this.state.selectArm}
          loadEnd={this.loadEnd}
          startDate={this.state.selectStartDate}
          endDate={this.state.selectEndDate}
          xaxis={this.state.selectXaxis}
          yaxis={this.state.selectYaxis}
          datashader={this.state.datashader}
          spectrograph={this.state.selectSpectrograph}
          datePeriod={this.state.datePeriod}
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
  };

  renderTabs = () => {
    const { tab } = this.state;
    return (
      <div>
        <Tabs
          value={tab}
          onChange={this.handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
        >
          <Tab label="Time Series" value={'Time Series'} />
          <Tab label="Regression" value={'Regression'} />
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
        {this.renderTimeSeries()}
      </Paper>
    );
  }
}

export default withStyles(styles)(TrendAnalysis);
