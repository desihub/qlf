import React from 'react';
import Sidemenu from '../../../src/screens/side-menu/side-menu';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import sinon from 'sinon';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { Link } from 'react-router-dom';
import { store, history } from '../../../src/store';
import { ConnectedRouter } from 'react-router-redux';
import { Provider } from 'react-redux';

configure({ adapter: new Adapter() });

describe('Sidemenu', () => {
  let sidemenu;
  it('renders', () => {
    const openDrawer = true;
    const closeDrawer = sinon.spy();
    sidemenu = (
      <Provider store={store}>
        <ConnectedRouter history={history}>
          <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
            <Sidemenu openDrawer={openDrawer} closeDrawer={closeDrawer} />
          </MuiThemeProvider>
        </ConnectedRouter>
      </Provider>
    );
    mount(sidemenu);
  });

  it('tests links', () => {
    const wrapper = mount(sidemenu);
    wrapper
      .find(Link)
      .at(0)
      .simulate('click');
    wrapper
      .find(Link)
      .at(1)
      .simulate('click');
    wrapper
      .find(Link)
      .at(2)
      .simulate('click');
  });
});
