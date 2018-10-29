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
      flavor: 'science',
    },
    datemjd: 58484.916666666664,
    runtime: '110.648429',
    qa_tests: [
      {
        r0: {
          fiberfl: { steps_status: ['NORMAL', 'NORMAL', 'NORMAL', 'NORMAL'] },
          preproc: { steps_status: ['NORMAL', 'NORMAL', 'NORMAL', 'NORMAL'] },
          extract: { steps_status: ['NORMAL'] },
          skysubs: { steps_status: ['NORMAL'] },
        },
      },
    ],
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
      flavor: 'science',
    },
    datemjd: 58484.916666666664,
    runtime: '96.254038',
    qa_tests: [
      {
        r0: {
          fiberfl: { steps_status: ['NORMAL', 'NORMAL', 'NORMAL', 'NORMAL'] },
          preproc: { steps_status: ['NORMAL', 'NORMAL', 'NORMAL', 'NORMAL'] },
          extract: { steps_status: ['NORMAL'] },
          skysubs: { steps_status: ['None'] },
        },
      },
    ],
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
          limit={10}
          type={'process'}
        />
      </MuiThemeProvider>
    );
    wrapper = mount(tableHistory);
  });

  it('Render processing history header', () => {
    expect(
      wrapper
        .find('span')
        .at(0)
        .text()
    ).toBe('Status');
    expect(
      wrapper
        .find('span')
        .at(1)
        .text()
    ).toBe('Program');
    expect(
      wrapper
        .find('span')
        .at(2)
        .text()
    ).toBe('Process ID');
    expect(
      wrapper
        .find('span')
        .at(3)
        .text()
    ).toBe('Exp ID');
    expect(
      wrapper
        .find('span')
        .at(4)
        .text()
    ).toBe('Flavor');
    expect(
      wrapper
        .find('span')
        .at(5)
        .text()
    ).toBe('Tile ID');
    expect(
      wrapper
        .find('span')
        .at(6)
        .text()
    ).toBe('Process Date');
    expect(
      wrapper
        .find('span')
        .at(7)
        .text()
    ).toBe('Process Time');
    expect(
      wrapper
        .find('span')
        .at(8)
        .text()
    ).toBe('OBS Date');
    expect(
      wrapper
        .find('span')
        .at(9)
        .text()
    ).toBe('MJD');
    expect(
      wrapper
        .find('span')
        .at(10)
        .text()
    ).toBe('RA (deg)');
    expect(
      wrapper
        .find('span')
        .at(11)
        .text()
    ).toBe('Dec (deg)');
    expect(
      wrapper
        .find('span')
        .at(12)
        .text()
    ).toBe('Exp Time(s)');
    expect(
      wrapper
        .find('span')
        .at(13)
        .text()
    ).toBe('Airmass');
    expect(
      wrapper
        .find('span')
        .at(14)
        .text()
    ).toBe('FWHM (arcsec)');
    expect(
      wrapper
        .find('span')
        .at(15)
        .text()
    ).toBe('QA');
    expect(
      wrapper
        .find('span')
        .at(16)
        .text()
    ).toBe('View');
    expect(
      wrapper
        .find('span')
        .at(17)
        .text()
    ).toBe('COM');
    expect(
      wrapper
        .find('span')
        .at(18)
        .text()
    ).toBe('Logs');
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

  it('calls navigateToQA error', async () => {
    await wrapper
      .find('TableCell')
      .at(53)
      .find('span')
      .at(0)
      .simulate('click');
    expect(
      wrapper
        .find('TableCell')
        .at(53)
        .find('span')
        .at(0)
        .text()
    ).toBe('✖︎');
    expect(navigateToQA).toBeCalledWith('70');
  });

  it('calls navigateToQA ok', async () => {
    await wrapper
      .find('TableCell')
      .at(34)
      .find('span')
      .at(0)
      .simulate('click');
    expect(
      wrapper
        .find('TableCell')
        .at(34)
        .find('span')
        .at(0)
        .text()
    ).toBe('✓');
    expect(navigateToQA).toBeCalledWith('69');
  });
});
