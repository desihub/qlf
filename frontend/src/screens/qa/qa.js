import React, { Component } from 'react';
import Steps from './widgets/steps/steps';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-around',
    flexDirection: 'column',
    marginBottom: '1vh',
    flex: 1,
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

  render() {
    return <div style={styles.container}>{this.renderSteps()}</div>;
  }
}

export default withStyles(styles)(QA);
