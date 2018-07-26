import React from 'react';
import CameraLog from '../../../src/screens/camera-log/camera-log';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('CameraLog', () => {
  let cameraLog;
  beforeEach(() => {
    cameraLog = <CameraLog cameraIndex={1} arm={'b'} lines={[]} />;
  });

  it('mounts', () => {
    mount(cameraLog);
  });
});
