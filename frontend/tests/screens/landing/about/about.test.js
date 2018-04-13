import AboutUs from '../../../../src/screens/landing/widgets/about/about';
import { mount, configure } from 'enzyme';
import React from 'react';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('Landing AboutUs', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <AboutUs />;
      </MuiThemeProvider>
    );
  });

  it('mounts', () => {
    const about = mount(wrapper);
    expect(about.find('h1').text()).toBe('About LIneA');
  });
});
