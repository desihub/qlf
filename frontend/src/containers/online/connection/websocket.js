import React, { Component } from 'react';
import Websocket from 'react-websocket';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {
  updateLastProcessAndMonitor,
  updateCameraState,
  updateQA,
} from '../online-store';

class Connection extends Component {
  static propTypes = {
    getWebsocketRef: PropTypes.func.isRequired,
    updateLastProcessAndMonitor: PropTypes.func.isRequired,
    updateCameraState: PropTypes.func.isRequired,
    updateQA: PropTypes.func.isRequired,
  };

  handleData = data => {
    const result = JSON.parse(data);
    if (result.lines) {
      const state = {
        daemonStatus: result.daemon_status
          ? 'Running'
          : result.daemon_status === false ? 'Not Running' : 'Idle',
        mainTerminal: result.lines ? result.lines.reverse() : [],
        ingestionTerminal:
          result.ingestion && result.ingestion !== 'Error'
            ? result.ingestion.reverse()
            : [],
        exposure: result.exposure.toString(),
        camerasStages: result.cameras,
        availableCameras: result.available_cameras,
        mjd: result.mjd === '' ? '' : result.mjd.toFixed(5),
        date: result.date === '' ? '' : result.date.split('T')[0],
        time: result.date === '' ? '' : result.date.split('T')[1],
        processId: result.process_id,
      };
      if (result.qa_results && result.qa_results.qa_tests) {
        this.props.updateQA({ qaTests: result.qa_results.qa_tests });
      }
      this.props.updateLastProcessAndMonitor(state);
    } else if (result.cameralog) {
      this.props.updateCameraState({ cameraTerminal: result.cameralog });
    }
  };

  storeWebsocketRef = socket => {
    this.socket = socket;
    this.props.getWebsocketRef(socket);
  };

  render() {
    const url = process.env.REACT_APP_WEBSOCKET;
    return (
      <div>
        <Websocket
          ref={this.storeWebsocketRef}
          url={url}
          onMessage={this.handleData}
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
}))(Connection);
