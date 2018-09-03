import React from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
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
import SelectDate from './select-date/select-date';

const styles = {
  controlsContainer: {
    display: 'grid',
    alignItems: 'start',
    width: '20em',
    justifyContent: 'start',
    borderRight: '1px solid darkgrey',
    overflowY: 'auto',
    paddingRight: '10px',
    boxSizing: 'border-box',
    height: 'calc(100vh - 200px)',
  },
  controlsContainerInner: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'left',
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
    width: 'calc(100vw - 390px)',
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
    width: '50%',
  },
  formControl: {
    width: '100%',
  },
  slice: {
    marginRight: '.5vw',
  },
  button: {
    float: 'right',
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

class TrendAnalysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tab: 'Time Series',
      arm: null,
      amp: '',
      loading: false,
      firstLoad: false,
      xaxis: '',
      yaxis: '',
      startDate: '',
      endDate: '',
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    startDate: PropTypes.string.isRequired,
    endDate: PropTypes.string.isRequired,
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value });
    this.loadStart();
  };

  handleChangeAmp = evt => {
    this.setState({ amp: evt.target.value });
    this.loadStart();
  };

  handleChangeXaxis = evt => {
    this.setState({ xaxis: evt.target.value });
    this.loadStart();
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
    const showControls =
      this.state.arm || this.state.amp || this.state.xaxis || this.state.yaxis;
    const classLoading = showControls
      ? styles.fadeLoader
      : styles.fadeLoaderFull;

    if (
      (this.state.tab === 'Time Series' &&
        this.state.amp !== '' &&
        this.state.yaxis !== '') ||
      (this.state.tab === 'Regression' &&
        this.state.amp !== '' &&
        this.state.yaxis !== '' &&
        this.state.xaxis !== '')
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

  clearSelection = () => {
    this.setState({
      arm: null,
      amp: '',
      xaxis: '',
      yaxis: '',
      loading: false,
    });
  };

  renderXaxisSelection = () => {
    if (this.state.tab !== 'Time Series')
      return (
        <div className={this.props.classes.selection}>
          <div className={this.props.classes.slice}>
            <FormControl className={this.props.classes.formControl}>
              <InputLabel shrink htmlFor="age-label-placeholder">
                Xaxis
              </InputLabel>
              <Select
                value={this.state.xaxis}
                onChange={this.handleChangeXaxis}
                input={<Input />}
                displayEmpty
                className={this.props.classes.selectEmpty}
              >
                <MenuItem value={'noise'}>Noise</MenuItem>
                <MenuItem value={'bias'}>Bias</MenuItem>
                <MenuItem value={'peakcount'}>Peakcount</MenuItem>
              </Select>
            </FormControl>
          </div>
        </div>
      );
  };

  renderYaxisSelection = () => {
    return (
      <div className={this.props.classes.selection}>
        <div className={this.props.classes.row}>
          <FormControl className={this.props.classes.formControl}>
            <InputLabel shrink htmlFor="age-label-placeholder">
              Yaxis
            </InputLabel>
            <Select
              value={this.state.yaxis}
              onChange={this.handleChangeYaxis}
              input={<Input />}
              displayEmpty
              className={this.props.classes.selectEmpty}
            >
              <MenuItem value={'noise'}>Noise</MenuItem>
              <MenuItem value={'bias'}>Bias</MenuItem>
              <MenuItem value={'peakcount'}>Peakcount</MenuItem>
            </Select>
          </FormControl>
        </div>
      </div>
    );
  };

  renderAmpSelection = () => {
    return (
      <div className={this.props.classes.selection}>
        <div className={this.props.classes.slice}>
          <FormControl className={this.props.classes.formControl}>
            <InputLabel shrink htmlFor="age-label-placeholder">
              Amp
            </InputLabel>
            <RadioGroup
              className={this.props.classes.column}
              value={this.state.amp}
              onChange={this.handleChangeAmp}
            >
              <FormControlLabel value="1" control={<Radio />} label="1" />
              <FormControlLabel value="2" control={<Radio />} label="2" />
              <FormControlLabel value="3" control={<Radio />} label="3" />
              <FormControlLabel value="4" control={<Radio />} label="4" />
            </RadioGroup>
          </FormControl>
        </div>
      </div>
    );
  };

  // renderArmSelection = () => {
  //   return (
  //     <div className={this.props.classes.selection}>
  //       <div className={this.props.classes.row}>
  //         <FormControl className={this.props.classes.formControl}>
  //           <InputLabel shrink htmlFor="age-label-placeholder">
  //             Arm
  //           </InputLabel>
  //           <RadioGroup
  //             className={this.props.classes.column}
  //             value={this.state.arm}
  //             onChange={this.handleChangeArm}
  //           >
  //             <FormControlLabel value="b" control={<Radio />} label="b" />
  //             <FormControlLabel value="r" control={<Radio />} label="r" />
  //             <FormControlLabel value="z" control={<Radio />} label="z" />
  //           </RadioGroup>
  //         </FormControl>
  //       </div>
  //     </div>
  //   );
  // };

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
          startDate={this.props.startDate}
          endDate={this.props.endDate}
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
        {this.renderSelectDate()}
        <div className={classes.controlsContainerInner}>
          {this.renderXaxisSelection()}
          {this.renderYaxisSelection()}
        </div>
        <div className={classes.controlsContainerInner}>
          {this.renderAmpSelection()}
          {/*this.renderArmSelection()*/}
        </div>
        {this.renderClear()}
      </div>
    );
  };

  renderViewer = plot => {
    return (
      <TrendViewer
        plot={plot}
        amp={this.state.amp}
        arm={this.state.arm}
        loadEnd={this.loadEnd}
        startDate={this.state.startDate}
        endDate={this.state.endDate}
        xaxis={this.state.xaxis}
        yaxis={this.state.yaxis}
      />
    );
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
        {this.renderTabs()}
      </Paper>
    );
  }
}

export default withStyles(styles)(TrendAnalysis);
