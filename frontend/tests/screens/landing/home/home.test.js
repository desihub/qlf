import Home from '../../../../src/screens/landing/widgets/home/home';
import { mount, configure } from 'enzyme';
import React from 'react';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('Landing Home', () => {
  let wrapper;
  const updateUrl = jest.fn();

  beforeEach(() => {
    const home = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Home updateUrl={updateUrl} />;
      </MuiThemeProvider>
    );
    wrapper = mount(home);
  });

  afterEach(() => {
    updateUrl.mockReset();
    wrapper.unmount();
  });

  it('has all cads completed', () => {
    expect(
      wrapper
        .find('a')
        .at(0)
        .text()
    ).toBe(
      'Pipeline MonitorControl and monitor the execution of the Quick Look pipeline'
    );
    expect(
      wrapper
        .find('a')
        .at(1)
        .text()
    ).toBe('QAMonitor QA metrics and provide access to diagnostic plots');
    expect(
      wrapper
        .find('a')
        .at(2)
        .text()
    ).toBe('Processing HistoryList exposures that have been processed');
    expect(
      wrapper
        .find('a')
        .at(3)
        .text()
    ).toBe(
      'Observing HistoryDisplay time series plots for QA metrics, list of exposures and observed targets for the current night of for a range of nights'
    );
    expect(
      wrapper
        .find('a')
        .at(4)
        .text()
    ).toBe(
      'Afternoon PlanningBrowse QA results for exposures processed by the offline pipeline at NERSC'
    );
    expect(
      wrapper
        .find('a')
        .at(5)
        .text()
    ).toBe(
      'Trend AnalysisSimple plots using quantities stored in the database'
    );
    expect(
      wrapper
        .find('a')
        .at(6)
        .text()
    ).toBe(
      'Sky ConditionsDisplay sky conditions such as atmospheric transparency, seeing, and sky background from the GFA camera'
    );
    expect(
      wrapper
        .find('a')
        .at(7)
        .text()
    ).toBe('Survey ReportsShow the overall progress and performance of survey');
    expect(
      wrapper
        .find('a')
        .at(8)
        .text()
    ).toBe('ConfigurationConfiguration of initial settings for execution');
  });

  it('resizes screen', () => {
    global.innerWidth = 500;
    global.dispatchEvent(new Event('resize'));
  });

  it('navigates to /monitor-realtime', () => {
    wrapper
      .find('a')
      .at(0)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/monitor-realtime');
  });

  it('navigates to /qa', () => {
    wrapper
      .find('a')
      .at(1)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/qa-realtime');
  });

  it('navigates to /processing-history', () => {
    wrapper
      .find('a')
      .at(2)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/processing-history');
  });

  it('navigates to /observing-history', () => {
    wrapper
      .find('a')
      .at(3)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/observing-history');
  });

  it('navigates to /', () => {
    wrapper
      .find('a')
      .at(4)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/');
    updateUrl.mockReset();
    wrapper
      .find('a')
      .at(5)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/');
    updateUrl.mockReset();
    wrapper
      .find('a')
      .at(6)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/');
    updateUrl.mockReset();
    wrapper
      .find('a')
      .at(7)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/');
    updateUrl.mockReset();
    wrapper
      .find('a')
      .at(8)
      .simulate('click');
    expect(updateUrl).toBeCalledWith('/');
  });
});
