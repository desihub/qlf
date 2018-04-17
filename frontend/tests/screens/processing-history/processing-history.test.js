import React from 'react';
import ProcessingHistory from '../../../src/screens/processing-history/processing-history';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

const processes = [
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

describe('ProcessingHistory Controls', () => {
  const getProcessingHistory = jest.fn(),
    getProcessingHistoryOrdered = jest.fn(() => processes),
    navigateToQA = jest.fn();
  let processingHistory;
  beforeEach(() => {
    window.getSelection = () => {
      return {
        removeAllRanges: () => {},
      };
    };
    processingHistory = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <ProcessingHistory
          processes={processes}
          getProcessingHistory={getProcessingHistory}
          navigateToQA={navigateToQA}
          getProcessingHistoryOrdered={getProcessingHistoryOrdered}
        />
      </MuiThemeProvider>
    );
  });

  it('mounts', () => {
    mount(processingHistory);
  });
});
