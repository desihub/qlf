import React from 'react';
import Controls from '../../../../../src/screens/monitor/widgets/controls/controls';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

let result;
function send(message) {
  result = message;
}

const socket = {
  state: {
    ws: {
      send: msg => send(msg),
    },
  },
};

describe('Controls', () => {
  let controls, controlsMount;
  beforeEach(() => {
    controlsMount = mount(<Controls socket={socket} />);
    controls = controlsMount.find('Button');
  });

  it('starts pipeline', () => {
    controls.at(0).simulate('mousedown');
    expect(result).toEqual('startPipeline');
  });
});
