import React, { Component } from 'react';
import Monitor from '../../screens/monitor/monitor';
import Websocket from './connection/websocket';
import QA from '../../screens/qa/qa';
import { Route } from 'react-router';
import Metrics from '../../screens/metrics/metrics';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {
  navigateToOnlineMetrics,
  navigateToOnlineQA,
  updateCameraState,
  updateWebsocket,
} from './online-store';
import { navigateToProcessingHistory } from '../offline/offline-store';
import CameraLog from '../../screens/camera-log/camera-log';

import _ from 'lodash';

const arms = ['b', 'r', 'z'];
const spectrographs = _.range(0, 10);

class OnlineContainer extends Component {
  static propTypes = {
    exposureId: PropTypes.string.isRequired,
    qaTests: PropTypes.array,
    arms: PropTypes.array.isRequired,
    spectrographs: PropTypes.array.isRequired,
    mjd: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired,
    navigateToMetrics: PropTypes.func.isRequired,
    daemonRunning: PropTypes.bool.isRequired,
    pipelineRunning: PropTypes.string.isRequired,
    mainTerminal: PropTypes.array.isRequired,
    ingestionTerminal: PropTypes.array.isRequired,
    cameraTerminal: PropTypes.array.isRequired,
    camerasStages: PropTypes.object.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    pathname: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func.isRequired,
    processId: PropTypes.string,
    arm: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired,
    spectrograph: PropTypes.number.isRequired,
    connected: PropTypes.func.isRequired,
    disconnected: PropTypes.func.isRequired,
    resetCameraLog: PropTypes.func.isRequired,
    updateWebsocket: PropTypes.func.isRequired,
    online: PropTypes.bool,
  };

  state = {
    socket: {},
    isOnline: false,
    updateCameraLog: true,
    cameraLogArm: '',
    cameraLogSpectrograph: '',
  };

  getWebsocketRef = socket => {
    this.setState({ socket });
  };

  componentWillReceiveProps() {
    if (window.location.pathname === '/camera-log') {
      if (
        window.location.search.includes('arm=') &&
        window.location.search.includes('cam=')
      ) {
        const spectrograph = window.location.search
          .substring(1)
          .split('&')[0]
          .split('=')[1];
        const arm = window.location.search
          .substring(1)
          .split('&')[1]
          .split('=')[1];
        this.setState({
          cameraLogArm: arm,
          cameraLogSpectrograph: spectrograph,
        });
      }
    }

    if (this.props.online && this.state.updateCameraLog) {
      this.setState({
        updateCameraLog: false,
      });
      this.state.socket.state.ws.send(
        `camera:${this.state.cameraLogArm}${this.state.cameraLogSpectrograph}`
      );
    }
  }

  isConnected = () => {
    this.props.updateWebsocket({ online: true });
    this.props.connected();
  };

  isDisconnected = () => {
    this.props.updateWebsocket({ online: false });
    this.props.disconnected();
  };

  startWebsocket = () => {
    return (
      <Websocket
        connected={this.isConnected}
        disconnected={this.isDisconnected}
        getWebsocketRef={this.getWebsocketRef}
      />
    );
  };

  navigateToCamera = (arm, cameraIndex) => {
    window.open(
      `camera-log?cam=${cameraIndex}&arm=${arm}`,
      'camera-log',
      'width=850, height=550'
    );
  };

  render() {
    return (
      <div>
        {this.startWebsocket()}
        <Route
          path="/camera-log"
          render={() => (
            <CameraLog
              cameraTerminal={this.props.cameraTerminal}
              websocketRef={this.state.socket}
              arm={this.state.cameraLogArm}
              cameraIndex={this.state.cameraLogSpectrograph}
              lines={this.props.cameraTerminal}
              online={this.props.online}
            />
          )}
        />
        <Route
          path="/monitor-realtime"
          render={() => (
            <Monitor
              socketRef={this.state.socket}
              exposureId={this.props.exposureId}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              daemonRunning={this.props.daemonRunning}
              pipelineRunning={this.props.pipelineRunning}
              mainTerminal={this.props.mainTerminal}
              ingestionTerminal={this.props.ingestionTerminal}
              cameraTerminal={this.props.cameraTerminal}
              camerasStages={this.props.camerasStages}
              processId={this.props.processId}
              arms={arms}
              spectrographs={spectrographs}
              qaTests={this.props.qaTests}
              resetCameraLog={this.props.resetCameraLog}
              navigateToCamera={this.navigateToCamera}
            />
          )}
        />
        <Route
          path="/qa-realtime"
          render={() => (
            <QA
              exposureId={this.props.exposureId}
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
              exposureId={this.props.exposureId}
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
    exposureId: state.qlfOnline.exposureId,
    qaTests: state.qlfOnline.qaTests,
    arms: state.qlfOnline.arms,
    spectrographs: state.qlfOnline.spectrographs,
    mjd: state.qlfOnline.mjd,
    date: state.qlfOnline.date,
    time: state.qlfOnline.time,
    daemonRunning: state.qlfOnline.daemonRunning,
    pipelineRunning: state.qlfOnline.pipelineRunning,
    mainTerminal: state.qlfOnline.mainTerminal,
    ingestionTerminal: state.qlfOnline.ingestionTerminal,
    cameraTerminal: state.qlfOnline.cameraTerminal,
    camerasStages: state.qlfOnline.camerasStages,
    pathname: state.router.location ? state.router.location.pathname : null,
    processId: state.qlfOnline.processId,
    arm: state.qlfOnline.arm,
    step: state.qlfOnline.step,
    spectrograph: state.qlfOnline.spectrograph,
    online: state.qlfOnline.online,
  }),
  dispatch => ({
    navigateToMetrics: (step, spectrograph, arm, exp) =>
      dispatch(navigateToOnlineMetrics(step, spectrograph, arm, exp)),
    navigateToProcessingHistory: () => dispatch(navigateToProcessingHistory()),
    navigateToQA: () => dispatch(navigateToOnlineQA()),
    resetCameraLog: () => dispatch(updateCameraState([])),
    updateWebsocket: state => dispatch(updateWebsocket(state)),
  })
)(OnlineContainer);
