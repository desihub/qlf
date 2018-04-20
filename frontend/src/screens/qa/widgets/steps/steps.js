import React, { Component } from 'react';
import PieChart from './piechart/piechart';
import { Card } from 'material-ui/Card';
import PropTypes from 'prop-types';
import ReactTooltip from 'react-tooltip';
import Status from '../../../../components/status/status';
import RaisedButton from 'material-ui/RaisedButton';

const steps = ['preproc', 'extract', 'fiberfl', 'skysubs'];
const stepsQa = {
  preproc: ['countpix', 'getbias', 'getrms', 'xwsigma'],
  extract: ['countbins'],
  fiberfl: ['integ', 'skycont', 'skypeak', 'skyresid'],
  skysubs: ['snr'],
};

let petalSize = window.innerWidth + window.innerHeight;

const styles = {
  container: {
    flex: 1,
    display: 'flex',
  },
  card: {
    borderLeft: 'solid 4px teal',
    flex: '1',
    height: '90%',
    paddingBottom: '1em',
  },
  containerSteps: {
    display: 'flex',
    justifyContent: 'space-around',
    paddingTop: '1em',
    alignItems: 'center',
  },
  arm: {
    fontWeight: 'bold',
    fontSize: 'calc(1.2vh + 1.2vw)',
    textAlign: 'center',
    flex: 1,
  },
  step: {
    width: 100,
    fontSize: 'calc(1vh + 1vw)',
    textAlign: 'center',
  },
  space: {
    width: '1vw',
    flex: 1,
  },
  processingHistoryButton: {
    margin: 'calc(0.8vh + 0.8vw)',
  },
  processingHistoryLabel: {
    paddingTop: '1vh',
    fontWeight: '900',
    fontSize: 'calc(0.6vh + 0.6vw)',
  },
  qaControls: {
    flexDirection: 'row',
    display: 'flex',
    alignItems: 'center',
  },
};

export default class Steps extends Component {
  static propTypes = {
    layout: PropTypes.object.isRequired,
    renderMetrics: PropTypes.func.isRequired,
    exposure: PropTypes.string,
    qaTests: PropTypes.array.isRequired,
    mjd: PropTypes.string,
    date: PropTypes.string,
    time: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func,
    petalSizeFactor: PropTypes.number.isRequired,
  };

  state = {
    message: '',
  };

  findQATest = arm => {
    if (this.props.qaTests.length !== 0) {
      const testKeys = this.props.qaTests.map(
        test => Object.keys(test).filter(key => key.includes(arm))[0]
      );
      const qaTests = this.props.qaTests.filter(test => {
        return testKeys.includes(Object.keys(test)[0]);
      });
      return qaTests;
    }
  };

  showQaAlarms = (camera, step) => {
    const cameraQa = this.props.qaTests.find(test => {
      if (Object.keys(test)[0] === camera) return test[camera];
      return null;
    });
    let message = '';
    if (cameraQa) {
      if (cameraQa[camera][steps[step]]) {
        cameraQa[camera][steps[step]].steps_status.forEach((val, idx) => {
          message +=
            stepsQa[steps[step]][idx] + ': ' + val.toLowerCase() + ' \n';
        });
      }
    }
    this.setState({ message });
  };

  hideQaAlarms = () => {};

  showStepName = name => {
    this.setState({ message: name + '\n' });
  };

  renderStep = (step, title, name) => {
    return (
      <div style={{ ...styles.containerSteps, ...this.props.layout }}>
        <span
          data-tip="true"
          data-for="tooltip"
          onMouseOver={() => this.showStepName(name)}
          style={styles.step}
        >
          {this.props.navigateToProcessingHistory ? name : title}
        </span>
        <PieChart
          renderMetrics={this.props.renderMetrics}
          step={step}
          arm={0}
          size={petalSize}
          showQaAlarms={this.showQaAlarms}
          hideQaAlarms={this.hideQaAlarms}
          qaTests={this.findQATest('b')}
        />
        <PieChart
          renderMetrics={this.props.renderMetrics}
          step={step}
          arm={1}
          size={petalSize}
          showQaAlarms={this.showQaAlarms}
          hideQaAlarms={this.hideQaAlarms}
          qaTests={this.findQATest('r')}
        />
        <PieChart
          renderMetrics={this.props.renderMetrics}
          step={step}
          arm={2}
          size={petalSize}
          showQaAlarms={this.showQaAlarms}
          hideQaAlarms={this.hideQaAlarms}
          qaTests={this.findQATest('z')}
        />
      </div>
    );
  };

  renderArms = () => {
    return this.props.layout.flexDirection === 'row' ? (
      <div style={{ ...styles.containerSteps, ...this.props.layout }}>
        <span style={styles.space}> </span>
        <span style={styles.arm}>b</span>
        <span style={styles.arm}>r</span>
        <span style={styles.arm}>z</span>
      </div>
    ) : null;
  };

  renderTooltipContent = () => {
    const message = this.state.message.split('\n').map((msg, i) => {
      return <p key={i}>{msg}</p>;
    });
    return message;
  };

  renderTooltip = () => {
    return (
      <ReactTooltip
        id="tooltip"
        type="info"
        getContent={this.renderTooltipContent}
      />
    );
  };

  renderHistoryControls = () => {
    if (!this.props.navigateToProcessingHistory) return;
    return (
      <div style={styles.qaControls}>
        <RaisedButton
          label={'Processing History'}
          secondary={true}
          style={styles.processingHistoryButton}
          labelStyle={styles.processingHistoryLabel}
          onClick={this.props.navigateToProcessingHistory}
        />
        <Status
          exposure={this.props.exposure}
          mjd={this.props.mjd}
          layout={this.props.layout}
          date={this.props.date}
          time={this.props.time}
        />
      </div>
    );
  };

  render() {
    petalSize =
      (window.innerWidth + window.innerHeight) / this.props.petalSizeFactor;
    return (
      <div>
        {this.renderTooltip()}
        {this.renderHistoryControls()}
        <Card style={styles.card}>
          {this.renderStep(0, 'Step 1', 'Pre Processing')}
          {this.renderStep(1, 'Step 2', 'Spectral Extraction')}
          {this.renderStep(2, 'Step 3', 'Fiber Flattening')}
          {this.renderStep(3, 'Step 4', 'Sky Subtraction')}
          {this.renderArms()}
        </Card>
      </div>
    );
  }
}
