import React from 'react';
import Controls from '../../../../../src/screens/monitor/widgets/controls/controls';
import { shallow, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import RaisedButton from 'material-ui/RaisedButton';

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
  let controls, controlsShallow;
  beforeEach(() => {
    controlsShallow = shallow(<Controls socket={socket} />);
    controls = controlsShallow.find(RaisedButton);
  });

  it('starts pipeline', () => {
    controls.at(0).simulate('mousedown');
    expect(result).toEqual('startPipeline');
  });

  it('stops pipeline', () => {
    controls.at(1).simulate('mousedown');
    expect(result).toEqual('resetPipeline');
  });
});
