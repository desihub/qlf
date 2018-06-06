import React from 'react';
import ImageModal from '../../../../../src/screens/history/widgets/image-modal/image-modal';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('ImageModal', () => {
  let imageModal;
  beforeEach(() => {
    imageModal = (
      <ImageModal
        startDate={'2019-01-01T22:00:00Z'}
        endDate={'2019-01-01T22:00:00Z'}
      />
    );
  });

  it('mounts', () => {
    mount(imageModal);
  });
});
