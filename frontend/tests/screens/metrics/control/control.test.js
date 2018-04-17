import React from 'react';
import Control from '../../../../src/screens/metrics/control/control';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import sinon from 'sinon';
import FlatButton from 'material-ui/FlatButton';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('Metric Controls', () => {
  let controls, changeArm;
  beforeEach(() => {
    changeArm = sinon.spy();
    controls = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Control change={changeArm} title={'Arm'} value={'b'} />
      </MuiThemeProvider>
    );
  });

  it('mounts', () => {
    mount(controls);
  });

  it('has select buttons', () => {
    const wrapper = mount(controls);
    const buttons = wrapper.find(FlatButton);
    buttons.at(0).simulate('click');
    buttons.at(1).simulate('click');
    expect(changeArm.callCount).toBe(2);
  });
});
