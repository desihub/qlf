import React from 'react';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { store } from '../../../src/store';
import { Provider } from 'react-redux';
import OnlineContainer from '../../../src/containers/online/online-container';
import { BrowserRouter as Router } from 'react-router-dom';
import { Server } from 'mock-socket';

configure({ adapter: new Adapter() });

const mockServer = new Server('ws://localhost:8000');

const setURL = url => {
  const parser = document.createElement('a');
  parser.href = url;
  [
    'href',
    'protocol',
    'host',
    'hostname',
    'origin',
    'port',
    'pathname',
    'search',
    'hash',
  ].forEach(prop => {
    Object.defineProperty(window.location, prop, {
      value: parser[prop],
      writable: true,
    });
  });
};

describe('OnlineContainer', () => {
  it('renders without crashing', () => {
    const online = (
      <Provider store={store}>
        <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
          <Router>
            <OnlineContainer />
          </Router>
        </MuiThemeProvider>
      </Provider>
    );
    mockServer.send(
      '{"date": "dateTtime", "mjd": 58484.916666666664, "upstream_status": false, "exposure": 4, "lines": ["2017-11-23 12:59:04 [INFO]: QLF Daemon status: False"], "daemon_status": false}'
    );
    mount(online);
  });

  it('renders monitor', () => {
    setURL('http://localhost:3000/monitor-realtime');
  });

  it('renders qa-realtime', () => {
    setURL('http://localhost:3000/qa-realtime');
  });
});
