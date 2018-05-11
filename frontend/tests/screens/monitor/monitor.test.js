import React from 'react';
import Monitor from '../../../src/screens/monitor/monitor';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { configure, mount, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { store } from '../../../src/store';
import { Provider } from 'react-redux';
import _ from 'lodash';

const arms = ['b', 'r', 'z'];
const spectrographs = _.range(0, 10);
configure({ adapter: new Adapter() });

const socket = {
  state: {
    ws: {
      send: jest.fn(),
    },
  },
};

describe('Monitor', () => {
  let wrapper;
  it('renders without crashing', () => {
    const monitor = (
      <Provider store={store}>
        <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
          <Monitor
            exposure={'3'}
            qaTests={[]}
            cameraTerminal={store.getState().qlfOnline.cameraTerminal}
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
    wrapper = mount(monitor);
  });

  it('receives props', async () => {
    const wrapper = shallow(
      <Monitor
        exposure={'3'}
        qaTests={[]}
        cameraTerminal={store.getState().qlfOnline.cameraTerminal}
        ingestionTerminal={[]}
        camerasStages={{}}
        daemonStatus={'Running'}
        arms={arms}
        spectrographs={spectrographs}
        socketRef={socket}
      />
    );
    const state = { cameraTerminal: ['New line'] };
    await store.dispatch({ type: 'UPDATE_CAMERA_STATE', state });
    wrapper.setProps({
      cameraTerminal: store.getState().qlfOnline.cameraTerminal,
    });
    expect(wrapper.state().cameraTerminal[0]).toBe('New line');
  });

  it('opens dialog', async () => {
    window.getSelection = () => {
      return {
        removeAllRanges: () => {},
      };
    };
    await wrapper
      .find('span')
      .at(40)
      .simulate('click');
    expect(socket.state.ws.send).toHaveBeenCalledWith('camera:z2');
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
