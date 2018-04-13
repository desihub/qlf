import Help from '../../../../src/screens/landing/widgets/help/help';
import { mount, configure } from 'enzyme';
import React from 'react';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('Landing Help', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Help />;
      </MuiThemeProvider>
    );
  });

  it('mounts', () => {
    const help = mount(wrapper);
    expect(
      help
        .find('h1')
        .at(0)
        .text()
    ).toBe('About the Quick Look Framework (QLF)');
  });
});
