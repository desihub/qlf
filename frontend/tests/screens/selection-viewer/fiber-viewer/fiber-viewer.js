import React from 'react';
import FiberViewer from '../../../../src/screens/selection-viewer/fiber-viewer/fiber-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('FiberViewer', () => {
  let fiberViewer;
  beforeEach(() => {
    fiberViewer = (
      <FiberViewer loadStart={jest.fn()} loadEnd={jest.fn()} loading={false} />
    );
  });

  it('mounts', () => {
    mount(fiberViewer);
  });
});
