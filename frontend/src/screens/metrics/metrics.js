import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Control from './control/control';
import MetricSelect from './metric-select/metric-select';
import Iframe from 'react-iframe';
import { FadeLoader } from 'halogenium';
import RaisedButton from 'material-ui/RaisedButton';
import Status from '../../components/status/status';

const styles = {
  container: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    paddingTop: '2vh',
    paddingBottom: '2vh',
  },
  controlsContainerLeft: {
    flex: 1,
    display: 'flex',
    flexDirection: 'row',
  },
  controlsContainerRight: {
    flex: 2,
    display: 'flex',
    flexDirection: 'column',
  },
  controls: {
    flex: 1,
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
  },
  loading: {
    display: 'flex',
    marginTop: '3em',
    justifyContent: 'center',
  },
  backButton: {
    margin: '1vw',
    width: 'calc(5px + 1vh)',
  },
};

const steps = [
  'Pre Processing',
  'Spectral Extraction',
  'Fiber Flattening',
  'Sky Subtraction',
];

export default class Metrics extends Component {
  static propTypes = {
    exposure: PropTypes.string,
    arms: PropTypes.array,
    spectrographs: PropTypes.array,
    qa: PropTypes.string,
    navigateToQA: PropTypes.func,
    qaTests: PropTypes.array,
    mjd: PropTypes.string,
    date: PropTypes.string,
    time: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func.isRequired,
  };

  state = {
    step: 0,
    spectrograph: 0,
    arm: 0,
    loading: false,
    qa: undefined,
  };

  componentWillMount() {
    if (this.props.exposure === '') this.props.navigateToProcessingHistory();
  }

  changeStep = direction => {
    this.setState({ qa: undefined, loading: false });
    if (direction === 'next') {
      this.setState({ step: Math.abs((this.state.step + 1) % steps.length) });
    } else {
      this.setState({
        step: Math.abs((this.state.step + steps.length - 1) % steps.length),
      });
    }
  };

  changeArm = direction => {
    this.startLoading();
    const length = this.props.arms.length;
    if (direction === 'next') {
      this.setState({ arm: Math.abs((this.state.arm + 1) % length) });
    } else {
      this.setState({
        arm: Math.abs((this.state.arm + length - 1) % length),
      });
    }
  };

  changeQA = qa => {
    this.setState({ qa, loading: true });
  };

  changeSpectrograph = direction => {
    this.startLoading();
    const length = this.props.spectrographs.length;
    const spectrograph =
      direction === 'next'
        ? Math.abs((this.state.spectrograph + 1) % length)
        : Math.abs((this.state.spectrograph + length - 1) % length);
    this.setState({
      spectrograph,
    });
  };

  startLoading = () => {
    if (this.state.qa !== undefined) this.setState({ loading: true });
  };

  endLoading = () => {
    this.setState({ loading: false });
  };

  iframeSize = () => {
    return window.innerWidth ? window.innerWidth * 0.8 : 1100;
  };

  onLoad = () => {
    this.endLoading();
  };

  storeIframeRef = ref => {
    if (ref) ref.refs.iframe.onload = this.onLoad;
  };

  renderLoading = () => {
    if (!this.state.loading) return null;
    return (
      <div style={{ ...styles.loading }}>
        <FadeLoader color="teal" size="16px" margin="4px" />
      </div>
    );
  };

  renderQA = () => {
    if (!this.state.qa) return;
    const height = this.iframeSize().toString();
    const url =
      process.env.REACT_APP_BOKEH +
      `${this.state.qa}/?exposure=${this.props.exposure}&arm=${
        this.props.arms[this.state.arm]
      }&spectrograph=${this.state.spectrograph}`;

    return (
      <div style={{ ...styles.controls }}>
        <Iframe
          url={url}
          ref={this.storeIframeRef}
          width="95%"
          height={height}
          display="initial"
          position="relative"
          allowFullScreen
        />
      </div>
    );
  };

  selectQA = qa => {
    this.changeQA(qa);
  };

  render() {
    const camera = this.props.arms[this.state.arm] + this.state.spectrograph;
    return (
      <div style={{ ...styles.container }}>
        <div style={{ ...styles.controlsContainerLeft }}>
          <MetricSelect
            camera={camera}
            selectedQA={this.props.qa}
            qaTests={this.props.qaTests}
            selectQA={this.selectQA}
            step={steps[this.state.step]}
          />
          <div style={{ ...styles.controlsContainerRight }}>
            <Status
              exposure={this.props.exposure}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
            />
            <div style={{ ...styles.controls }}>
              <Control
                change={this.changeStep}
                title={'Step'}
                value={steps[this.state.step]}
              />
              <Control
                change={this.changeSpectrograph}
                title={'Spectrograph'}
                value={this.state.spectrograph}
              />
              <Control
                change={this.changeArm}
                title={'Arm'}
                value={this.props.arms[this.state.arm]}
              />
              <RaisedButton
                label={'Steps'}
                secondary={true}
                style={styles.backButton}
                onClick={this.props.navigateToQA}
              />
            </div>
          </div>
        </div>
        {this.renderLoading()}
        {this.renderQA()}
      </div>
    );
  }
}
