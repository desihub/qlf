import React from 'react';
import MetricSelect from '../../../../src/screens/metrics/metric-select/metric-select';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import sinon from 'sinon';

configure({ adapter: new Adapter() });

describe('Metric Controls', () => {
  let metricSelect, selectQA;
  beforeEach(() => {
    selectQA = sinon.spy();
    metricSelect = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <MetricSelect
          step={'Pre Processing'}
          selectQA={selectQA}
          camera={'b0'}
          qaTests={[]}
        />
      </MuiThemeProvider>
    );
  });

  it('mounts', () => {
    mount(metricSelect);
  });
});
