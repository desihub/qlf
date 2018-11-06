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
          pipelineRunning={'Running'}
          exposureId={'3'}
        />
      </MuiThemeProvider>
    );
    mount(status);
  });

  it('unmounts', () => {
    const wrapper = mount(status);
    expect(
      wrapper
        .find('CardContent')
        .at(2)
        .text()
    ).toBe('Exposure: 3');
    expect(
      wrapper
        .find('CardContent')
        .at(0)
        .text()
    ).toBe('Status: Running');
    wrapper.unmount();
  });
});
