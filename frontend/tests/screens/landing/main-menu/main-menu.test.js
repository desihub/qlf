import MainMenu from '../../../../src/screens/landing/widgets/main-menu/main-menu';
import React from 'react';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { BrowserRouter as Router } from 'react-router-dom';

configure({ adapter: new Adapter() });

describe('MainMenu', () => {
  let wrapper;

  const mainMenu = screen => {
    return (
      <Router>
        <MainMenu currentScreen={screen} />
      </Router>
    );
  };

  afterEach(() => {
    wrapper.unmount();
  });

  it('makes home screen menu italic', () => {
    wrapper = mount(mainMenu('/'));
    wrapper.find('Link').forEach((link, idx) => {
      if (idx === 0) expect(link.props().style.fontStyle).toBe('italic');
      else expect(link.props().style.fontStyle).toBe(undefined);
    });
  });

  it('makes about screen menu italic', () => {
    wrapper = mount(mainMenu('/about'));
    wrapper.find('Link').forEach((link, idx) => {
      if (idx === 1) expect(link.props().style.fontStyle).toBe('italic');
      else expect(link.props().style.fontStyle).toBe(undefined);
    });
  });

  it('makes help screen menu italic', () => {
    wrapper = mount(mainMenu('/help'));
    wrapper.find('Link').forEach((link, idx) => {
      if (idx === 2) expect(link.props().style.fontStyle).toBe('italic');
      else expect(link.props().style.fontStyle).toBe(undefined);
    });
  });

  it('makes tutorials screen menu italic', () => {
    wrapper = mount(mainMenu('/tutorials'));
    wrapper.find('Link').forEach((link, idx) => {
      if (idx === 3) expect(link.props().style.fontStyle).toBe('italic');
      else expect(link.props().style.fontStyle).toBe(undefined);
    });
  });

  it('makes contact screen menu italic', () => {
    wrapper = mount(mainMenu('/contact'));
    wrapper.find('Link').forEach((link, idx) => {
      if (idx === 4) expect(link.props().style.fontStyle).toBe('italic');
      else expect(link.props().style.fontStyle).toBe(undefined);
    });
  });
});
