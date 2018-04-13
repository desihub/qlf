import Contact from '../../../../src/screens/landing/widgets/contact/contact';
import { mount, configure } from 'enzyme';
import React from 'react';
import Adapter from 'enzyme-adapter-react-16';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

describe('Landing Contact', () => {
  let wrapper;

  beforeEach(() => {
    const contact = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Contact />;
      </MuiThemeProvider>
    );
    wrapper = mount(contact);
  });

  it('mounts', () => {
    expect(wrapper.find('h1').text()).toBe('Contact Us');
  });

  it('sends incompleted form', () => {
    wrapper
      .find('RaisedButton')
      .find('button')
      .simulate('click');
    expect(
      wrapper
        .find('TextField')
        .at(0)
        .text()
    ).toBe('NameRequired');
  });
});
