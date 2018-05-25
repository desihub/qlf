import React, { Component } from 'react';
import Steps from './widgets/steps/steps';
import PropTypes from 'prop-types';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-around',
    flexDirection: 'column',
    marginBottom: '1vh',
    flex: 1,
  },
};

export default class QA extends Component {
  static propTypes = {
    exposure: PropTypes.string,
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
        this.props.exposure
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
        exposure={this.props.exposure}
        date={this.props.date}
        time={this.props.time}
        petalSizeFactor={this.props.petalSizeFactor}
        processId={this.props.processId}
        monitor={this.props.monitor}
      />
    );
  };

  render() {
    return <div style={styles.container}>{this.renderSteps()}</div>;
  }
}
