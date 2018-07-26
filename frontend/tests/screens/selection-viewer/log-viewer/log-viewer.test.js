import React from 'react';
import LogViewer from '../../../../src/screens/selection-viewer/log-viewer/log-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('LogViewer', () => {
  let logViewer;
  beforeEach(() => {
    logViewer = (
      <LogViewer loadStart={jest.fn()} loadEnd={jest.fn()} loading={false} />
    );
  });

  it('mounts', () => {
    mount(logViewer);
  });
});
