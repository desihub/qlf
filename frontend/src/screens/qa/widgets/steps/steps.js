import React, { Component } from 'react';
import PieChart from './piechart/piechart';
import { Card } from 'material-ui/Card';
import PropTypes from 'prop-types';
import ReactTooltip from 'react-tooltip';
import Status from '../../../../components/status/status';
import Tooltip from '@material-ui/core/Tooltip';
import { withStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';

const steps = ['preproc', 'extract', 'fiberfl', 'skysubs'];
const stepsQa = {
  preproc: ['countpix', 'getbias', 'getrms', 'xwsigma'],
  extract: ['countbins'],
  fiberfl: ['skycont', 'skypeak'],
  skysubs: ['integ', 'skyresid', 'snr'],
};

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
    borderLeft: 'solid 4px #424242',
    flex: '1',
  },
  containerSteps: {
    display: 'flex',
    justifyContent: 'space-around',
    paddingTop: '1em',
    alignItems: 'center',
    flexDirection: 'row',
  },
  containerLegend: {
    position: 'relative',
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
  icon: {
    position: 'absolute',
    top: '1px',
    left: '1px',
    cursor: 'pointer',
  },
  green: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: '#008000',
    fontSize: 0,
    textIndent: '-9999em',
  },
  yellow: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: '#ffff00',
    fontSize: 0,
    textIndent: '-9999em',
  },
  red: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: '#ff0000',
    fontSize: 0,
    textIndent: '-9999em',
  },
  lightgray: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: '#d3d3d3',
    fontSize: 0,
    textIndent: '-9999em',
  },
  black: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: '#000000',
    fontSize: 0,
    textIndent: '-9999em',
  },
};

class Steps extends Component {
  static propTypes = {
    renderMetrics: PropTypes.func.isRequired,
    exposureId: PropTypes.string,
    qaTests: PropTypes.array,
    mjd: PropTypes.string,
    date: PropTypes.string,
    time: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func,
    petalSizeFactor: PropTypes.number.isRequired,
    processId: PropTypes.number,
    monitor: PropTypes.bool,
    flavor: PropTypes.string,
  };

  state = {
    message: '',
    petalSize: 80,
  };

  componentWillMount() {
    if (!this.props.monitor)
      window.addEventListener('resize', this.updatePetalSize);
  }

  componentDidMount() {
    if (!this.props.monitor) this.updatePetalSize();
  }

  componentWillUnmount() {
    if (!this.props.monitor)
      window.removeEventListener('resize', this.updatePetalSize);
  }

  updatePetalSize = () => {
    if (window.outerWidth) {
      this.setState({
        petalSize:
          (window.outerWidth + window.outerHeight) / this.props.petalSizeFactor,
      });
    }
  };

  findQATest = arm => {
    if (this.props.qaTests) {
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
    if (!this.props.qaTests) return;
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
        size={this.state.petalSize}
        showQaAlarms={this.showQaAlarms}
        hideQaAlarms={this.hideQaAlarms}
        qaTests={this.findQATest(arms[arm])}
        monitor={this.props.monitor}
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
          exposureId={this.props.exposureId}
          mjd={this.props.mjd}
          date={this.props.date}
          time={this.props.time}
          flavor={this.props.flavor}
          processId={String(this.props.processId)}
        />
      </div>
    );
  };

  renderLegendColor = () => {
    return (
      <div>
        <p>
          <span style={styles.green}>Green</span> All tests passed
        </p>
        <p>
          <span style={styles.yellow}>Yellow</span> Warning on one or more QA
          test
        </p>
        <p>
          <span style={styles.red}>Red</span> Error on one or more QA test
        </p>
        <p>
          <span style={styles.lightgray}>Lightgray</span> QA test file not
          generated
        </p>
        <p>
          <span style={styles.black}>Black</span> Pipeline not completed
        </p>
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
            <div style={styles.containerLegend}>
              <Tooltip title={this.renderLegendColor()} placement="bottom">
                <Icon style={styles.icon}>info</Icon>
              </Tooltip>
            </div>
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

export default withStyles(styles)(Steps);
