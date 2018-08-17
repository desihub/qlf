import React, { Component } from 'react';
import Steps from './widgets/steps/steps';
import PropTypes from 'prop-types';
import Tooltip from '@material-ui/core/Tooltip';
import { withStyles } from '@material-ui/core/styles';
import { Info } from 'material-ui-icons';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-around',
    flexDirection: 'column',
    marginBottom: '1vh',
    flex: 1,
    position: 'relative',
  },
  icon: {
    position: 'absolute',
    top: 0,
    left: '5px',
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

class QA extends Component {
  static propTypes = {
    exposureId: PropTypes.string,
    qaTests: PropTypes.array,
    arms: PropTypes.array.isRequired,
    spectrographs: PropTypes.array.isRequired,
    mjd: PropTypes.string,
    date: PropTypes.string,
    time: PropTypes.string,
    navigateToMetrics: PropTypes.func,
    navigateToProcessingHistory: PropTypes.func,
    petalSizeFactor: PropTypes.number.isRequired,
    processId: PropTypes.number,
    monitor: PropTypes.bool,
    flavor: PropTypes.string,
  };

  componentDidMount() {
    document.title = 'QA';
  }

  renderMetrics = (step, spectrographNumber, arm) => {
    if (this.props.navigateToMetrics) {
      this.props.navigateToMetrics(
        step,
        spectrographNumber,
        arm,
        this.props.exposureId
      );
    }
  };

  renderSteps = () => {
    return (
      <Steps
        navigateToProcessingHistory={this.props.navigateToProcessingHistory}
        qaTests={this.props.qaTests}
        renderMetrics={this.renderMetrics}
        mjd={this.props.mjd}
        exposureId={this.props.exposureId}
        date={this.props.date}
        time={this.props.time}
        petalSizeFactor={this.props.petalSizeFactor}
        processId={this.props.processId}
        monitor={this.props.monitor}
        flavor={this.props.flavor}
      />
    );
  };

  renderLegendColor = () => {
    return (
      <div>
        <p>
          <span style={styles.green}>Green</span>: All tests passed
        </p>
        <p>
          <span style={styles.yellow}>Yellow</span>: Warning on one or more QA
          test
        </p>
        <p>
          <span style={styles.red}>Red</span>: Error on one or more QA test
        </p>
        <p>
          <span style={styles.lightgray}>Lightgray</span>: QA test file not
          generated
        </p>
        <p>
          <span style={styles.black}>Black</span>: Pipeline not completed
        </p>
      </div>
    );
  };

  render() {
    return (
      <div style={styles.container}>
        <Tooltip title={this.renderLegendColor()} placement="bottom">
          <Info style={styles.icon} />
        </Tooltip>
        {this.renderSteps()}
      </div>
    );
  }
}

export default withStyles(styles)(QA);
