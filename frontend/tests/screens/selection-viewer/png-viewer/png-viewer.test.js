import React from 'react';
import PNGPreview from '../../../../src/screens/selection-viewer/png-preview/png-preview';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('PNGPreview', () => {
  let pngPreview;
  beforeEach(() => {
    pngPreview = <PNGPreview loadEnd={jest.fn()} spectrograph={[0]} />;
  });

  it('mounts', () => {
    mount(pngPreview);
  });
});
