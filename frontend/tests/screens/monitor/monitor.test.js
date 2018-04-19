import React from 'react';
import Monitor from '../../../src/screens/monitor/monitor';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { store } from '../../../src/store';
import { Provider } from 'react-redux';
import _ from 'lodash';

const arms = ['b', 'r', 'z'];
const spectrographs = _.range(0, 9);
configure({ adapter: new Adapter() });

function send(message) {
  return message;
}

const socket = {
  state: {
    ws: {
      send: msg => send(msg),
    },
  },
};

describe('Monitor', () => {
  it('renders without crashing', () => {
    const monitor = (
      <Provider store={store}>
        <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
          <Monitor
            exposure={'3'}
            qaTests={[]}
            cameraTerminal={[]}
            ingestionTerminal={[]}
            camerasStages={{}}
            daemonStatus={'Running'}
            arms={arms}
            spectrographs={spectrographs}
            socketRef={socket}
          />
        </MuiThemeProvider>
      </Provider>
    );
    mount(monitor);
  });

  it('resizes screen', () => {
    const monitor = (
      <Provider store={store}>
        <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
          <Monitor
            exposure={'3'}
            qaTests={[]}
            cameraTerminal={[]}
            ingestionTerminal={[]}
            camerasStages={{}}
            daemonStatus={'Running'}
            arms={arms}
            spectrographs={spectrographs}
            socketRef={socket}
          />
        </MuiThemeProvider>
      </Provider>
    );
    mount(monitor);
    global.innerWidth = 500;
    global.dispatchEvent(new Event('resize'));
  });
});
