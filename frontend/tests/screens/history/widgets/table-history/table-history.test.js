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
    exposure: {
      dateobs: '2019-01-01T22:00:00Z',
      exposure_id: 3,
      tile: 6,
      telra: 333.22,
      teldec: 14.84,
      exptime: 1000,
      airmass: null,
    },
    datemjd: 58484.916666666664,
    runtime: '110.648429',
  },
  {
    pk: 70,
    exposure: {
      dateobs: '2019-01-01T22:00:00Z',
      exposure_id: 4,
      tile: 7,
      telra: 332.35,
      teldec: 12.32,
      exptime: 1000,
      airmass: null,
    },
    datemjd: 58484.916666666664,
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

  it('calls navigateToQA', async () => {
    await wrapper
      .find('TableCell')
      .at(32)
      .find('span')
      .at(0)
      .simulate('click');
    expect(
      wrapper
        .find('TableCell')
        .at(32)
        .find('span')
        .at(0)
        .text()
    ).toBe('✖︎');
    expect(navigateToQA).toBeCalledWith(69);
  });
});
