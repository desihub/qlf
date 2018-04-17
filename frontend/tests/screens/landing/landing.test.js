import React from 'react';
import Landing from '../../../src/screens/landing/landing';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { BrowserRouter as Router } from 'react-router-dom';
import sinon from 'sinon';

configure({ adapter: new Adapter() });

describe('Landing', () => {
  const func = sinon.spy();
  let landing, wrapper;

  beforeEach(() => {
    landing = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Router>
          <Landing updateUrl={func} />
        </Router>
      </MuiThemeProvider>
    );
    wrapper = mount(landing);
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('does not navigate', () => {
    wrapper
      .find('a')
      .at(2)
      .simulate('click');
    expect(window.location.pathname).toBe('/');
  });
});
