import React from 'react';
import PieChart from '../../../../../src/screens/qa/widgets/steps/piechart/piechart';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { VictoryPie } from 'victory';
import sinon from 'sinon';

configure({ adapter: new Adapter() });

describe('QA', () => {
  let piechart;
  it('renders without crashing', () => {
    const renderMetrics = sinon.spy();
    const showQaAlarms = sinon.spy();
    const hideQaAlarms = sinon.spy();
    piechart = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <PieChart
          renderMetrics={renderMetrics}
          arm={0}
          step={0}
          size={150}
          showQaAlarms={showQaAlarms}
          hideQaAlarms={hideQaAlarms}
          qaTests={[]}
        />
      </MuiThemeProvider>
    );
    mount(piechart);
  });

  it('test events', () => {
    const wrapper = mount(piechart);
    expect(
      wrapper
        .find(VictoryPie)
        .find('path')
        .at(0)
        .props().style.fill
    ).toBe('gray');
    wrapper
      .find(VictoryPie)
      .find('path')
      .at(0)
      .simulate('mouseover');
    expect(
      wrapper
        .find(VictoryPie)
        .find('path')
        .at(0)
        .props().style.fill
    ).toBe('gray');
    wrapper
      .find(VictoryPie)
      .find('path')
      .at(0)
      .simulate('mouseout');
    wrapper
      .find(VictoryPie)
      .find('path')
      .at(0)
      .simulate('click');
  });
});
