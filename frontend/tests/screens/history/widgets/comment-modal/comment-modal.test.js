import React from 'react';
import CommentModal from '../../../../../src/screens/history/widgets/comment-modal/comment-modal';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('CommentModal', () => {
  let commentModal;
  beforeEach(() => {
    commentModal = (
      <CommentModal
        startDate={'2019-01-01T22:00:00Z'}
        endDate={'2019-01-01T22:00:00Z'}
      />
    );
  });

  it('mounts', () => {
    mount(commentModal);
  });
});
