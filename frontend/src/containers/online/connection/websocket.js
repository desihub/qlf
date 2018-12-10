import React, { Component } from 'react';
import Websocket from './connection';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {
  updateLastProcessAndMonitor,
  updateCameraState,
  updateQA,
  updateNotifications,
} from '../online-store';

class Connection extends Component {
  static propTypes = {
    getWebsocketRef: PropTypes.func.isRequired,
    updateLastProcessAndMonitor: PropTypes.func.isRequired,
    updateCameraState: PropTypes.func.isRequired,
    updateQA: PropTypes.func.isRequired,
    updateNotifications: PropTypes.func.isRequired,
    connected: PropTypes.func.isRequired,
    disconnected: PropTypes.func.isRequired,
  };

  handleData = data => {
    const result = JSON.parse(data);

    if (result.notification) {
      const notification = JSON.parse(result.notification);
      this.props.updateNotifications(notification);
    }
    // console.log(result)

    if (result.lines) {
      const state = {
        pipelineRunning:
          result.pipeline_running === 2
            ? 'Running'
            : result.pipeline_running === 1 ? 'Idle' : 'Not Running',
        daemonRunning: result.daemon_running,
        mainTerminal: result.lines ? result.lines.reverse() : [],
        ingestionTerminal:
          result.ingestion && result.ingestion !== 'Error'
            ? result.ingestion.reverse()
            : [],
        exposureId: result.exposure.toString(),
        flavor: result.flavor,
        camerasStages: result.cameras,
        availableCameras: result.available_cameras,
        mjd: result.mjd === '' ? '' : result.mjd.toFixed(3),
        date: result.date === '' ? '' : result.date.split(' ')[0],
        time: result.date === '' ? '' : result.date.split(' ')[1],
        processId: result.process_id.toString(),
        qaTests: [],
      };
      if (result.qa_results && Array.isArray(result.qa_results)) {
        this.props.updateQA({ qaTests: result.qa_results });
      } else {
        this.props.updateQA({ qaTests: [] });
      }
      this.props.updateLastProcessAndMonitor(state);
    } else if (result.cameralog) {
      this.props.updateCameraState(result.cameralog);
    }
  };

  storeWebsocketRef = socket => {
    this.socket = socket;
    this.props.getWebsocketRef(socket);
  };

  render() {
    const url =
      process.env.NODE_ENV === 'development'
        ? process.env.REACT_APP_WEBSOCKET
        : window.origin.replace('http', 'ws') + '/dashboard/';

    return (
      <div>
        <Websocket
          ref={this.storeWebsocketRef}
          url={url}
          onMessage={this.handleData}
          onOpen={this.props.connected}
          onClose={this.props.disconnected}
          debug={true}
        />
      </div>
    );
  }
}

export default connect(null, dispatch => ({
  updateLastProcessAndMonitor: state =>
    dispatch(updateLastProcessAndMonitor(state)),
  updateCameraState: state => dispatch(updateCameraState(state)),
  updateQA: state => dispatch(updateQA(state)),
  updateNotifications: state => dispatch(updateNotifications(state)),
}))(Connection);
