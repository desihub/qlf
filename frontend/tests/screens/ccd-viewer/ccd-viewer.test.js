import React from 'react';
import CCDViewer from '../../../src/screens/ccd-viewer/ccd-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('CCDViewer', () => {
  let ccdViewer;
  beforeEach(() => {
    ccdViewer = <CCDViewer />;
  });

  it('mounts', () => {
    mount(ccdViewer);
  });
});
