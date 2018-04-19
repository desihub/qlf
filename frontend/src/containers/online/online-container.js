import React, { Component } from 'react';
import Monitor from '../../screens/monitor/monitor';
import Websocket from './connection/websocket';
import QA from '../../screens/qa/qa';
import { Route } from 'react-router';
import Metrics from '../../screens/metrics/metrics';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { navigateToOnlineMetrics, navigateToOnlineQA } from './online-store';
import { navigateToProcessingHistory } from '../offline/offline-store';

import _ from 'lodash';

const arms = ['b', 'r', 'z'];
const spectrographs = _.range(0, 9);

class OnlineContainer extends Component {
  static propTypes = {
    exposure: PropTypes.string.isRequired,
    qaTests: PropTypes.array.isRequired,
    arms: PropTypes.array.isRequired,
    spectrographs: PropTypes.array.isRequired,
    mjd: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired,
    navigateToMetrics: PropTypes.func.isRequired,
    daemonStatus: PropTypes.string.isRequired,
    ingestionTerminal: PropTypes.array.isRequired,
    cameraTerminal: PropTypes.array.isRequired,
    camerasStages: PropTypes.object.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    pathname: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func.isRequired,
    processId: PropTypes.number,
    arm: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired,
    spectrograph: PropTypes.number.isRequired,
  };

  state = {
    socket: {},
    isOnline: false,
  };

  getWebsocketRef = socket => {
    this.setState({ socket });
  };

  componentWillMount() {
    if (this.props.pathname && this.props.pathname.includes('realtime'))
      this.setState({ isOnline: true });
  }

  componentWillReceiveProps(nextProps) {
    if (
      this.props.pathname &&
      nextProps.pathname &&
      nextProps.pathname.includes('realtime') &&
      !this.props.pathname.includes('realtime')
    )
      this.setState({ isOnline: true });
    else if (
      this.props.pathname &&
      nextProps.pathname &&
      !nextProps.pathname.includes('realtime') &&
      this.props.pathname.includes('realtime')
    )
      this.setState({ isOnline: false });
  }

  startWebsocket = () => {
    if (this.state.isOnline)
      return <Websocket getWebsocketRef={this.getWebsocketRef} />;
  };

  render() {
    return (
      <div>
        {this.startWebsocket()}
        <Route
          path="/monitor-realtime"
          render={() => (
            <Monitor
              socketRef={this.state.socket}
              exposure={this.props.exposure}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              daemonStatus={this.props.daemonStatus}
              ingestionTerminal={this.props.ingestionTerminal}
              cameraTerminal={this.props.cameraTerminal}
              camerasStages={this.props.camerasStages}
              processId={this.props.processId}
              arms={arms}
              spectrographs={spectrographs}
              qaTests={this.props.qaTests}
            />
          )}
        />
        <Route
          path="/qa-realtime"
          render={() => (
            <QA
              exposure={this.props.exposure}
              qaTests={this.props.qaTests}
              arms={arms}
              spectrographs={spectrographs}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              navigateToProcessingHistory={
                this.props.navigateToProcessingHistory
              }
              navigateToMetrics={this.props.navigateToMetrics}
              petalSizeFactor={16}
            />
          )}
        />
        <Route
          path="/metrics-realtime"
          render={() => (
            <Metrics
              exposure={this.props.exposure}
              qaTests={this.props.qaTests}
              arms={arms}
              spectrographs={spectrographs}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              navigateToMetrics={this.props.navigateToMetrics}
              navigateToQA={this.props.navigateToQA}
              navigateToProcessingHistory={
                this.props.navigateToProcessingHistory
              }
              arm={this.props.arm}
              step={this.props.step}
              spectrograph={this.props.spectrograph}
            />
          )}
        />
      </div>
    );
  }
}

export default connect(
  state => ({
    exposure: state.qlfOnline.exposure,
    qaTests: state.qlfOnline.qaTests,
    arms: state.qlfOnline.arms,
    spectrographs: state.qlfOnline.spectrographs,
    mjd: state.qlfOnline.mjd,
    date: state.qlfOnline.date,
    time: state.qlfOnline.time,
    daemonStatus: state.qlfOnline.daemonStatus,
    ingestionTerminal: state.qlfOnline.ingestionTerminal,
    cameraTerminal: state.qlfOnline.cameraTerminal,
    camerasStages: state.qlfOnline.camerasStages,
    pathname: state.router.location ? state.router.location.pathname : null,
    processId: state.qlfOnline.processId,
    arm: state.qlfOnline.arm,
    step: state.qlfOnline.step,
    spectrograph: state.qlfOnline.spectrograph,
  }),
  dispatch => ({
    navigateToMetrics: (step, spectrograph, arm, exp) =>
      dispatch(navigateToOnlineMetrics(step, spectrograph, arm, exp)),
    navigateToProcessingHistory: () => dispatch(navigateToProcessingHistory()),
    navigateToQA: () => dispatch(navigateToOnlineQA()),
  })
)(OnlineContainer);
