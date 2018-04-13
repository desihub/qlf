import React from 'react';
import TableHistory from '../../../../../src/screens/processing-history/widgets/table-history/table-history';
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

describe('TableHistory Controls', () => {
  const getProcessingHistory = jest.fn(),
    getProcessingHistoryOrdered = jest.fn(() => processes),
    navigateToQA = jest.fn();
  let wrapper;
  beforeEach(() => {
    window.getSelection = () => {
      return {
        removeAllRanges: () => {},
      };
    };
    const tableHistory = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <TableHistory
          processes={processes}
          getProcessingHistory={getProcessingHistory}
          navigateToQA={navigateToQA}
          getProcessingHistoryOrdered={getProcessingHistoryOrdered}
        />
      </MuiThemeProvider>
    );
    wrapper = mount(tableHistory);
  });

  it('mounts rendering table', () => {
    expect(getProcessingHistory).toBeCalled();
    expect(
      wrapper
        .find('TableHeaderColumn')
        .at(0)
        .text()
    ).toBe('Process ID');
    expect(
      wrapper
        .find('TableRowColumn')
        .at(0)
        .text()
    ).toBe('69');
  });

  it('orders table', () => {
    wrapper
      .find('span')
      .at(0)
      .simulate('click');
    expect(getProcessingHistoryOrdered).toBeCalledWith('-pk');
    wrapper
      .find('span')
      .at(0)
      .simulate('click');
    expect(getProcessingHistoryOrdered).toBeCalledWith('-pk');
  });

  it('calls navigateToQA', () => {
    wrapper
      .find('span')
      .at(10)
      .simulate('click');
    expect(navigateToQA).toBeCalledWith(70);
  });
});
