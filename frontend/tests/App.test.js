import React from 'react';
import App from '../src/App';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { Server } from 'mock-socket';

configure({ adapter: new Adapter() });
process.env.REACT_APP_WEBSOCKET = 'ws://localhost:8000';
jest.mock('../src/assets/DESILogo.png', () => 'desilogo.png');

const mockServer = new Server('ws://localhost:8000');

mockServer.on('connection', () => {
  mockServer.send('test message 1');
});

describe('App', () => {
  let wrapper;

  beforeEach(() => {
    const app = <App />;
    wrapper = mount(app);
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('renders', () => {
    expect(
      wrapper
        .find('Link')
        .at(0)
        .text()
    ).toBe('Home');
  });
});
