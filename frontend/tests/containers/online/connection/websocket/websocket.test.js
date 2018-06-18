import React from 'react';
import Websocket from '../../../../../src/containers/online/connection/websocket';
import { Server } from 'mock-socket';
import { store } from '../../../../../src/store';
import { Provider } from 'react-redux';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

process.env.REACT_APP_WEBSOCKET = 'ws://localhost:8000';

const mockServer = new Server('ws://localhost:8000');

function getWebsocketRef() {
  return;
}

function updateState(result) {
  return result;
}

describe('Websocket', () => {
  it('renders without crashing', () => {
    const websocketScreen = (
      <Provider store={store}>
        <Websocket
          getWebsocketRef={getWebsocketRef}
          updateState={updateState}
        />
      </Provider>
    );
    mount(websocketScreen);
  });

  it('receives a state update from api', () => {
    mockServer.send(
      '{"process_id": 10, "date": "date time", "mjd": 58484.916666666664, "upstream_status": false, "exposure": 4, "ingestion": ["2017-11-23 12:59:04 [INFO]: QLF Daemon status: False"], "lines": ["2017-11-23 12:59:04 [INFO]: QLF Daemon status: False"], "pipeline_running": 0, "daemon_running": false}'
    );

    expect(store.getState().qlfOnline).toEqual({
      arms: [],
      spectrographs: [],
      cameraTerminal: [],
      camerasStages: undefined,
      daemonRunning: false,
      pipelineRunning: 'Not Running',
      exposureId: '4',
      ingestionTerminal: [
        '2017-11-23 12:59:04 [INFO]: QLF Daemon status: False',
      ],
      mainTerminal: ['2017-11-23 12:59:04 [INFO]: QLF Daemon status: False'],
      mjd: '58484.917',
      time: 'time',
      date: 'date',
      arm: 0,
      step: 0,
      spectrograph: 0,
      processId: '10',
      qaTests: [],
      notifications: [],
    });
  });

  it('receives a camera log update', () => {
    mockServer.send(
      '{"cameralog": ["2017-11-21 14:05:39,263 QuickLook INFO : Running Quicklook"]}'
    );

    expect(store.getState().qlfOnline).toEqual({
      arms: [],
      mjd: '58484.917',
      time: 'time',
      date: 'date',
      spectrographs: [],
      cameraTerminal: [
        '2017-11-21 14:05:39,263 QuickLook INFO : Running Quicklook',
      ],
      daemonRunning: false,
      pipelineRunning: 'Not Running',
      camerasStages: undefined,
      exposureId: '4',
      ingestionTerminal: [
        '2017-11-23 12:59:04 [INFO]: QLF Daemon status: False',
      ],
      mainTerminal: ['2017-11-23 12:59:04 [INFO]: QLF Daemon status: False'],
      qaTests: [],
      arm: 0,
      spectrograph: 0,
      step: 0,
      processId: '10',
      notifications: [],
    });
  });
});
