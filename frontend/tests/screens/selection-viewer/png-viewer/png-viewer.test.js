import React from 'react';
import PNGViewer from '../../../../src/screens/selection-viewer/png-viewer/png-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('PNGViewer', () => {
  let pngViewer;
  beforeEach(() => {
    pngViewer = <PNGViewer loadEnd={jest.fn()} spectrograph={[0]} />;
  });

  it('mounts', () => {
    mount(pngViewer);
  });
});
