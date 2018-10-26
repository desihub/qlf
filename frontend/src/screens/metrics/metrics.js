import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Control from './control/control';
import MetricSelect from './metric-select/metric-select';
import Iframe from 'react-iframe';
import { FadeLoader } from 'halogenium';
import Status from '../../components/status/status';
import flavors from '../../flavors';

const styles = {
  container: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    maxHeight: '115,5px',
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
    display: 'flex',
    alignItems: 'center',
    boxShadow: 'none',
  },
  grid: {
    flex: 1,
    display: 'grid',
    flexDirection: 'row',
    gridTemplateColumns: 'auto auto auto',
    marginRight: '1vw',
  },
};

export default class Metrics extends Component {
  static propTypes = {
    exposureId: PropTypes.string,
    arms: PropTypes.array,
    spectrographs: PropTypes.array,
    qa: PropTypes.string,
    navigateToQA: PropTypes.func,
    qaTests: PropTypes.array,
    mjd: PropTypes.string,
    date: PropTypes.string,
    time: PropTypes.string,
    flavor: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func.isRequired,
    arm: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired,
    spectrograph: PropTypes.number.isRequired,
    processId: PropTypes.number,
  };

  state = {
    step: this.props.step,
    spectrograph: this.props.spectrograph,
    arm: this.props.arm,
    loading: false,
    qa: undefined,
    steps: [],
    stepsQa: {},
  };

  componentWillMount() {
    if (this.props.exposureId === '') this.props.navigateToProcessingHistory();
    const steps = [];
    const stepsQa = {};
    if (flavors[this.props.flavor]) {
      flavors[this.props.flavor].step_list.map(step => {
        steps.push(step.name);
        stepsQa[step.name] = step.qa_list.map(qa => {
          return qa.display_name;
        });
        return null;
      });
      this.setState({ steps, stepsQa });
    }
  }

  componentDidMount() {
    document.title = 'Metrics';
  }

  changeStep = direction => {
    this.setState({ qa: undefined, loading: false });
    if (direction === 'next') {
      this.setState({
        step: Math.abs((this.state.step + 1) % this.state.steps.length),
      });
    } else {
      this.setState({
        step: Math.abs(
          (this.state.step + this.state.steps.length - 1) %
            this.state.steps.length
        ),
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

  changeQA = async qa => {
    if (this.state.qa === qa) await this.setState({ qa: '' });
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
        <FadeLoader color="#424242" size="16px" margin="4px" />
      </div>
    );
  };

  renderQA = () => {
    if (!this.state.qa) return;
    const url =
      process.env.REACT_APP_BOKEH +
      `load_qa/?qa=${this.state.qa}&process_id=${this.props.processId}&arm=${
        this.props.arms[this.state.arm]
      }&spectrograph=${this.state.spectrograph}`;

    return (
      <div style={{ ...styles.controls }}>
        <Iframe
          url={url}
          ref={this.storeIframeRef}
          width="100%"
          height="calc(100vh - 191px)"
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
    const step = this.state.steps[this.state.step]
      ? this.state.steps[this.state.step].toUpperCase()
      : undefined;
    return (
      <div style={{ ...styles.container }}>
        <div style={{ ...styles.controlsContainerLeft }}>
          <MetricSelect
            camera={camera}
            selectedQA={this.props.qa}
            qaTests={this.props.qaTests}
            selectQA={this.selectQA}
            step={this.state.steps[this.state.step]}
            back={this.props.navigateToQA}
            stepsQa={this.state.stepsQa}
          />
          <div style={{ ...styles.controlsContainerRight }}>
            <Status
              exposureId={this.props.exposureId}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              flavor={this.props.flavor}
            />
            <div style={styles.grid}>
              <Control change={this.changeStep} title={'Step'} value={step} />
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
            </div>
          </div>
        </div>
        {this.renderLoading()}
        {this.renderQA()}
      </div>
    );
  }
}
