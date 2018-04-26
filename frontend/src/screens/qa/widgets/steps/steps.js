import React, { Component } from 'react';
import PieChart from './piechart/piechart';
import { Card } from 'material-ui/Card';
import PropTypes from 'prop-types';
import ReactTooltip from 'react-tooltip';
import Status from '../../../../components/status/status';

const steps = ['preproc', 'extract', 'fiberfl', 'skysubs'];
const stepsQa = {
  preproc: ['countpix', 'getbias', 'getrms', 'xwsigma'],
  extract: ['countbins'],
  fiberfl: ['integ', 'skycont', 'skypeak', 'skyresid'],
  skysubs: ['snr'],
};

let petalSize = window.innerWidth + window.innerHeight;
const arms = ['b', 'r', 'z'];

const styles = {
  container: {
    flex: 1,
    display: 'grid',
    gridTemplateColumns: 'auto auto auto auto auto',
  },
  gridItem: {
    textAlign: 'center',
    alignItems: 'center',
    paddingBottom: '0.5vh',
  },
  gridArm: {
    paddingLeft: '1vw',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    borderLeft: 'solid 4px teal',
    flex: '1',
    height: '90%',
  },
  containerSteps: {
    display: 'flex',
    justifyContent: 'space-around',
    paddingTop: '1em',
    alignItems: 'center',
    flexDirection: 'row',
  },
  arm: {
    fontWeight: 'bold',
    fontSize: '14px',
    textAlign: 'center',
    flex: 1,
  },
  step: {
    width: 100,
    fontSize: '12px',
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
    fontSize: '14px',
  },
  qaControls: {
    flexDirection: 'row',
    display: 'flex',
    alignItems: 'center',
  },
};

export default class Steps extends Component {
  static propTypes = {
    renderMetrics: PropTypes.func.isRequired,
    exposure: PropTypes.string,
    qaTests: PropTypes.array.isRequired,
    mjd: PropTypes.string,
    date: PropTypes.string,
    time: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func,
    petalSizeFactor: PropTypes.number.isRequired,
    processId: PropTypes.number,
  };

  state = {
    message: '',
  };

  componentWillMount() {
    window.addEventListener('resize', this.updatePetalSize);
    this.updatePetalSize();
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updatePetalSize);
  }

  updatePetalSize = () => {
    petalSize =
      (window.outerWidth + window.outerHeight) / this.props.petalSizeFactor;
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

  renderPieChart = (arm, step) => {
    return (
      <PieChart
        renderMetrics={this.props.renderMetrics}
        step={step}
        arm={arm}
        size={petalSize}
        showQaAlarms={this.showQaAlarms}
        hideQaAlarms={this.hideQaAlarms}
        qaTests={this.findQATest(arms[arm])}
      />
    );
  };

  renderStepName = (title, name) => {
    return (
      <span
        data-tip="true"
        data-for="tooltip"
        onMouseOver={() => this.showStepName(name)}
        style={styles.step}
      >
        {this.props.navigateToProcessingHistory ? name : title}
      </span>
    );
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
        <Status
          exposure={this.props.exposure}
          mjd={this.props.mjd}
          date={this.props.date}
          time={this.props.time}
          processId={this.props.processId}
        />
      </div>
    );
  };

  render() {
    return (
      <div>
        {this.renderTooltip()}
        {this.renderHistoryControls()}
        <Card style={styles.card}>
          <div style={styles.container}>
            <div />
            <div style={styles.gridItem}>
              {this.renderStepName('Step 1', 'Pre Processing')}
            </div>
            <div style={styles.gridItem}>
              {this.renderStepName('Step 2', 'Spectral Extraction')}
            </div>
            <div style={styles.gridItem}>
              {this.renderStepName('Step 3', 'Fiber Flattening')}
            </div>
            <div style={styles.gridItem}>
              {this.renderStepName('Step 4', 'Sky Subtraction')}
            </div>
            <div style={styles.gridArm}>
              <span style={styles.arm}>b</span>
            </div>
            <div style={styles.gridItem}>{this.renderPieChart(0, 0)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(0, 1)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(0, 2)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(0, 3)}</div>
            <div style={styles.gridArm}>
              <span style={styles.arm}>r</span>
            </div>
            <div style={styles.gridItem}>{this.renderPieChart(1, 0)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(1, 1)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(1, 2)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(1, 3)}</div>
            <div style={styles.gridArm}>
              <span style={styles.arm}>z</span>
            </div>
            <div style={styles.gridItem}>{this.renderPieChart(2, 0)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(2, 1)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(2, 2)}</div>
            <div style={styles.gridItem}>{this.renderPieChart(2, 3)}</div>
          </div>
        </Card>
      </div>
    );
  }
}
