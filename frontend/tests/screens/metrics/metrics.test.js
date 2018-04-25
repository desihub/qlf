import React from 'react';
import Metrics from '../../../src/screens/metrics/metrics';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import _ from 'lodash';

const arms = ['b', 'r', 'z'];
const spectrographs = _.range(0, 10);
configure({ adapter: new Adapter() });

const qaTests = [
  {
    b0: {
      fiberfl: { steps_status: ['NORMAL', 'NORMAL', 'NORMAL', 'NORMAL'] },
      extract: { steps_status: ['NORMAL'] },
      preproc: { steps_status: ['NORMAL', 'NORMAL', 'NORMAL', 'NORMAL'] },
      skysubs: { steps_status: ['NORMAL'] },
    },
  },
];

describe('Metric Controls', () => {
  let metrics, navigateToProcessingHistory, navigateToQA, wrapper;
  beforeEach(() => {
    navigateToQA = jest.fn();
    navigateToProcessingHistory = jest.fn();
    metrics = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Metrics
          arms={arms}
          spectrographs={spectrographs}
          exposure={'3'}
          loading={false}
          navigateToQA={navigateToQA}
          qaTests={qaTests}
          mjd={'58484.91667'}
          time={'22:00:00'}
          date={'2019-01-01'}
          navigateToProcessingHistory={navigateToProcessingHistory}
          step={0}
          arm={0}
          spectrograph={0}
        />
      </MuiThemeProvider>
    );
    wrapper = mount(metrics);
  });

  it('changes step', () => {
    expect(
      wrapper
        .find('Control')
        .at(0)
        .text()
    ).toBe('Step<Pre Processing>');
    wrapper
      .find('FlatButton')
      .at(4)
      .simulate('click');
    expect(
      wrapper
        .find('Control')
        .at(0)
        .text()
    ).toBe('Step<Sky Subtraction>');
  });

  it('selects qa', () => {
    const countpixQa = wrapper.find('FlatButton').at(0);
    expect(countpixQa.text()).toBe('COUNTPIX ✓');
    countpixQa.simulate('click');
    expect(wrapper.find('Iframe').props().url).toBe(
      'http://localhost:8001/dashboard/qacountpix/?exposure=3&arm=b&spectrograph=0'
    );
  });
});
