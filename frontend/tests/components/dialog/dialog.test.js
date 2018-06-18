import React from 'react';
import ConfirmDialog from '../../../src/components/dialog/dialog';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('Confirm Dialog', () => {
  let wrapper;
  const handleClose = jest.fn(),
    onConfirm = jest.fn();

  beforeEach(() => {
    const dialog = (
      <ConfirmDialog
        title={'Confirmation'}
        subtitle={'Are you sure you want to confirm?'}
        handleClose={handleClose}
        onConfirm={onConfirm}
        open={true}
      />
    );
    wrapper = mount(dialog);
  });

  it('opens dialog', () => {
    expect(wrapper.find('DialogTitle').text()).toBe('Confirmation');
    expect(wrapper.find('DialogContentText').text()).toBe(
      'Are you sure you want to confirm?'
    );
    expect(
      wrapper
        .find('Button')
        .at(0)
        .text()
    ).toBe('Cancel');
    expect(
      wrapper
        .find('Button')
        .at(1)
        .text()
    ).toBe('Yes');
  });

  it('calls handle close on cancel click', () => {
    wrapper
      .find('Button')
      .at(0)
      .simulate('click');
    expect(handleClose).toHaveBeenCalled();
  });

  it('calls on confirm on ok click', () => {
    wrapper
      .find('Button')
      .at(1)
      .simulate('click');
    expect(onConfirm).toHaveBeenCalled();
    expect(handleClose).toHaveBeenCalled();
  });
});
