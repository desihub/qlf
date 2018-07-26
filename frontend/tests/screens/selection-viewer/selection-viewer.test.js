import React from 'react';
import SelectionViewer from '../../../src/screens/selection-viewer/selection-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('SelectionViewer', () => {
  let selectionViewer;
  beforeEach(() => {
    selectionViewer = <SelectionViewer />;
  });

  it('mounts', () => {
    mount(selectionViewer);
  });
});
