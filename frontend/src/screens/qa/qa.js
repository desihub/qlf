import React, { Component } from 'react';
import Steps from './widgets/steps/steps';
import PropTypes from 'prop-types';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-around',
    padding: '1vh 1vw 1vh 1vw',
    flexDirection: 'column',
    marginBottom: '1vh',
  },
};

export default class QA extends Component {
  static propTypes = {
    exposure: PropTypes.string,
    qaTests: PropTypes.array.isRequired,
    arms: PropTypes.array.isRequired,
    spectrographs: PropTypes.array.isRequired,
    mjd: PropTypes.string,
    date: PropTypes.string,
    time: PropTypes.string,
    navigateToMetrics: PropTypes.func,
    navigateToProcessingHistory: PropTypes.func,
    petalSizeFactor: PropTypes.number.isRequired,
    processId: PropTypes.number,
  };

  state = {
    layout: {},
    metrics: undefined,
    qaCameras: undefined,
  };

  componentDidMount() {
    this.updateWindowDimensions();
    window.addEventListener('resize', this.updateWindowDimensions);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updateWindowDimensions);
  }

  updateWindowDimensions = () => {
    this.setState({
      layout: {
        flexDirection: 'row',
      },
    });
  };

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
        layout={this.state.layout}
        mjd={this.props.mjd}
        exposure={this.props.exposure}
        date={this.props.date}
        time={this.props.time}
        petalSizeFactor={this.props.petalSizeFactor}
        processId={this.props.processId}
      />
    );
  };

  render() {
    return <div style={styles.container}>{this.renderSteps()}</div>;
  }
}
