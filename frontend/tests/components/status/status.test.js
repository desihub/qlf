import React from 'react';
import Status from '../../../src/components/status/status';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('Monitor Status', () => {
  let status;
  it('mounts', () => {
    status = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Status
          layout={{}}
          mjd={''}
          time={''}
          date={''}
          daemonStatus={'Running'}
          exposure={'3'}
        />
      </MuiThemeProvider>
    );
    mount(status);
  });

  it('unmounts', () => {
    const wrapper = mount(status);
    expect(
      wrapper
        .find('Cards')
        .at(2)
        .props().subtitle
    ).toBe('3');
    expect(
      wrapper
        .find('Cards')
        .at(0)
        .props().subtitle
    ).toBe('Running');
    wrapper.unmount();
  });
});
