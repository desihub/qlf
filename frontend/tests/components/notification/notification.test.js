import React from 'react';
import Notification from '../../../src/components/notification/notification';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { store } from '../../../src/store';
import { updateNotifications } from '../../../src/containers/online/online-store';
import { Provider } from 'react-redux';

configure({ adapter: new Adapter() });

describe('Monitor Status', () => {
  let wrapper;

  beforeEach(() => {
    const status = (
      <Provider store={store}>
        <Notification />
      </Provider>
    );
    wrapper = mount(status);
    store.dispatch(
      updateNotifications({
        type: 'Alert',
        text: 'Available Disk Space 8%',
        date: '2018-06-12 13:37:00 UTC',
      })
    );
  });

  it('opens notifications', async () => {
    expect(wrapper.find('ListItem').length).toBe(0);
    await wrapper.find('Badge').simulate('click');
    expect(wrapper.find('ListItem').length).toBe(1);
  });

  it('clears notifications', async () => {
    await wrapper.find('Badge').simulate('click');
    expect(wrapper.find('ListItem').length).toBe(2);
    expect(
      wrapper
        .find('h3')
        .at(0)
        .text()
    ).toBe('Available Disk Space 8%');
    await wrapper.find('Button').simulate('click');
    expect(wrapper.find('ListItem').length).toBe(0);
  });
});
