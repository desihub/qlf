import React from 'react';
import SelectDate from '../../../../../src/screens/history/widgets/select-date/select-date';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('SelectDate Controls', () => {
  let history;
  beforeEach(() => {
    history = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <SelectDate
          startDate={'2019-01-01T22:00:00Z'}
          endDate={'2019-01-01T22:00:00Z'}
        />
      </MuiThemeProvider>
    );
  });

  it('mounts', () => {
    mount(history);
  });
});
