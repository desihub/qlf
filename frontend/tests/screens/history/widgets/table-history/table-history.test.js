import React from 'react';
import TableHistory from '../../../../../src/screens/history/widgets/table-history/table-history';
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

describe('TableHistory Controls', () => {
  const getHistory = jest.fn(),
    getHistoryOrdered = jest.fn(() => rows),
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
          rows={rows}
          getHistory={getHistory}
          navigateToQA={navigateToQA}
          getHistoryOrdered={getHistoryOrdered}
          type={'process'}
        />
      </MuiThemeProvider>
    );
    wrapper = mount(tableHistory);
  });

  // it('mounts rendering table', () => {
  //   expect(getHistory).toBeCalled();
  //   expect(
  //     wrapper
  //       .find('TableHeaderColumn')
  //       .at(1)
  //       .text()
  //   ).toBe('Process ID');
  //   expect(
  //     wrapper
  //       .find('TableRowColumn')
  //       .at(1)
  //       .text()
  //   ).toBe('69');
  // });

  // it('orders table', () => {
  //   wrapper
  //     .find('span')
  //     .at(1)
  //     .simulate('click');
  //   expect(getHistoryOrdered).toBeCalledWith('-pk');
  //   wrapper
  //     .find('span')
  //     .at(0)
  //     .simulate('click');
  //   expect(getHistoryOrdered).toBeCalledWith('-pk');
  // });

  it('calls navigateToQA', () => {
    wrapper
      .find('span')
      .at(16)
      .simulate('click');
    expect(navigateToQA).toBeCalledWith(69);
  });
});
