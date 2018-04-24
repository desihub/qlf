import React from 'react';
import History from '../../../src/screens/history/history';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

const rows = [
  {
    pk: 69,
    dateobs: '2019-01-01T22:00:00Z',
    datemjd: 58484.916666666664,
    exposure_id: 3,
    tile: 6,
    telra: 333.22,
    teldec: 14.84,
    exptime: 1000,
    airmass: null,
    runtime: '110.648429',
  },
  {
    pk: 70,
    dateobs: '2019-01-01T22:00:00Z',
    datemjd: 58484.916666666664,
    exposure_id: 4,
    tile: 7,
    telra: 332.35,
    teldec: 12.32,
    exptime: 1000,
    airmass: null,
    runtime: '96.254038',
  },
];

describe('History Controls', () => {
  const getHistory = jest.fn(),
    getHistoryOrdered = jest.fn(() => rows),
    navigateToQA = jest.fn();
  let history;
  beforeEach(() => {
    window.getSelection = () => {
      return {
        removeAllRanges: () => {},
      };
    };
    history = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <History
          rows={rows}
          getHistory={getHistory}
          navigateToQA={navigateToQA}
          getHistoryOrdered={getHistoryOrdered}
          type={'process'}
        />
      </MuiThemeProvider>
    );
  });

  it('mounts', () => {
    mount(history);
  });
});
