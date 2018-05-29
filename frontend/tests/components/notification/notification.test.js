import React from 'react';
import Notification from '../../../src/components/notification/notification';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('Monitor Status', () => {
  let wrapper;

  beforeEach(() => {
    const status = <Notification />;
    wrapper = mount(status);
  });

  it('opens notifications', async () => {
    expect(wrapper.find('ListItem').length).toBe(0);
    await wrapper.find('Badge').simulate('click');
    expect(wrapper.find('ListItem').length).toBe(3);
  });

  it('clears notifications', async () => {
    await wrapper.find('Badge').simulate('click');
    expect(wrapper.find('ListItem').length).toBe(3);
    await wrapper.find('Button').simulate('click');
    expect(wrapper.find('ListItem').length).toBe(0);
  });
});
