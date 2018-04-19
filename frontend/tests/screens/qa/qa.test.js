import React from 'react';
import QA from '../../../src/screens/qa/qa';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { store } from '../../../src/store';
// import { store, updateMonitorState, updateQA } from '../../../src/store';
import { Provider } from 'react-redux';

configure({ adapter: new Adapter() });

const status = {
  exposure: '3',
  availableCameras: ['b0', 'b1', 'r0', 'r1', 'z0', 'z1'],
  mjd: '',
  time: '',
  date: '',
  arms: ['b', 'r'],
  spectrographs: [0, 1, 2],
};

const qaTests = [
  {
    camera: 'b0',
    qa_tests:
      "{'fiberfl': {'steps_status': ['FAILURE', 'FAILURE', 'FAILURE', 'FAILURE'], 'color': 'magenta'}, 'skysubs': {'steps_status': ['FAILURE'], 'color': 'magenta'}, 'extract': {'steps_status': ['FAILURE'], 'color': 'magenta'}, 'preproc': {'steps_status': ['FAILURE', 'NORMAL', 'FAILURE', 'FAILURE'], 'color': 'magenta'}}",
    spectrograph: '0',
    links: { self: 'http://localhost:8000/dashboard/api/camera/b0/' },
    arm: 'b',
  },
  {
    camera: 'b1',
    qa_tests:
      "{'fiberfl': {'steps_status': ['FAILURE', 'FAILURE', 'FAILURE', 'FAILURE'], 'color': 'magenta'}, 'skysubs': {'steps_status': ['FAILURE'], 'color': 'magenta'}, 'extract': {'steps_status': ['FAILURE'], 'color': 'magenta'}, 'preproc': {'steps_status': ['FAILURE', 'NORMAL', 'FAILURE', 'FAILURE'], 'color': 'magenta'}}",
    spectrograph: '1',
    links: { self: 'http://localhost:8000/dashboard/api/camera/b1/' },
    arm: 'b',
  },
  {
    camera: 'r0',
    qa_tests:
      "{'fiberfl': {'steps_status': ['FAILURE', 'FAILURE', 'FAILURE', 'FAILURE'], 'color': 'magenta'}, 'skysubs': {'steps_status': ['FAILURE'], 'color': 'magenta'}, 'extract': {'steps_status': ['FAILURE'], 'color': 'magenta'}, 'preproc': {'steps_status': ['FAILURE', 'NORMAL', 'FAILURE', 'FAILURE'], 'color': 'magenta'}}",
    spectrograph: '0',
    links: { self: 'http://localhost:8000/dashboard/api/camera/r0/' },
    arm: 'r',
  },
  {
    camera: 'r1',
    qa_tests:
      "{'fiberfl': {'steps_status': ['FAILURE', 'NORMAL', 'NORMAL', 'NORMAL'], 'color': 'magenta'}, 'skysubs': {'steps_status': ['NORMAL'], 'color': 'green'}, 'extract': {'steps_status': ['NORMAL'], 'color': 'green'}, 'preproc': {'steps_status': ['NORMAL', 'NORMAL', 'NORMAL', 'NORMAL'], 'color': 'green'}}",
    spectrograph: '1',
    links: { self: 'http://localhost:8000/dashboard/api/camera/r1/' },
    arm: 'r',
  },
];

describe('QA', () => {
  let qa, wrapper;

  beforeEach(() => {
    qa = (
      <Provider store={store}>
        <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
          <QA
            exposure={status.exposure}
            qaTests={qaTests}
            arms={status.arms}
            spectrographs={status.spectrographs}
            mjd={status.mjd}
            date={status.mjd}
            time={status.time}
            navigateToMetrics={jest.fn()}
            isOnline={jest.fn()}
            isOffline={jest.fn()}
            petalSizeFactor={16}
            navigateToProcessingHistory={jest.fn()}
          />
        </MuiThemeProvider>
      </Provider>
    );
    wrapper = mount(qa);
  });

  it('renders without crashing', () => {
    mount(qa);
  });

  it('changes store', async () => {
    expect(
      wrapper
        .find('Cards')
        .at(0)
        .props().subtitle
    ).toBe('3');
    expect(
      wrapper
        .find('path')
        .at(0)
        .props().style.fill
    ).toBe('gray');
    expect(
      wrapper
        .find('path')
        .at(2)
        .props().style.fill
    ).toBe('gray');
  });

  // it('enters qa second screen and change selection clicking on flatbutton', () => {
  //   wrapper
  //     .find('path')
  //     .at(0)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('FlatButton')
  //       .at(0)
  //       .text()
  //   ).toBe('COUNTPIX ✖︎');
  //   wrapper
  //     .find('FlatButton')
  //     .at(4)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('FlatButton')
  //       .at(0)
  //       .text()
  //   ).toBe('SNR ✖︎');
  // });

  // it('changes step', () => {
  //   wrapper
  //     .find('path')
  //     .at(0)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(0)
  //       .props().value
  //   ).toBe('Pre Processing');
  //   wrapper
  //     .find('FlatButton')
  //     .at(4)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(0)
  //       .props().value
  //   ).toBe('Sky Subtraction');
  //   wrapper
  //     .find('FlatButton')
  //     .at(2)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(0)
  //       .props().value
  //   ).toBe('Pre Processing');
  // });

  // it('changes spectrograph', () => {
  //   wrapper
  //     .find('path')
  //     .at(0)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(1)
  //       .props().value
  //   ).toBe('0');
  //   wrapper
  //     .find('FlatButton')
  //     .at(6)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(1)
  //       .props().value
  //   ).toBe('1');
  //   wrapper
  //     .find('FlatButton')
  //     .at(7)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(1)
  //       .props().value
  //   ).toBe('0');
  // });

  // it('changes arm', () => {
  //   wrapper
  //     .find('path')
  //     .at(0)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(2)
  //       .props().value
  //   ).toBe('b');
  //   wrapper
  //     .find('FlatButton')
  //     .at(8)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(2)
  //       .props().value
  //   ).toBe('z');
  //   wrapper
  //     .find('FlatButton')
  //     .at(9)
  //     .simulate('click');
  //   expect(
  //     wrapper
  //       .find('Control')
  //       .at(2)
  //       .props().value
  //   ).toBe('b');
  // });

  it('resizes', async () => {
    global.innerWidth = 2000;
    await global.dispatchEvent(new Event('resize'));
    global.innerWidth = 500;
    await global.dispatchEvent(new Event('resize'));
  });

  it('unmounts', () => {
    wrapper.unmount();
  });
});
