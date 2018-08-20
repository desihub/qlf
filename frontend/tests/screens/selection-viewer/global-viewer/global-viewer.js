import React from 'react';
import GlobalViewer from '../../../../src/screens/selection-viewer/global-viewer/global-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('GlobalViewer', () => {
  let globalViewer;
  beforeEach(() => {
    globalViewer = (
      <GlobalViewer
        screen={'globalfiber'}
        loadStart={jest.fn()}
        loadEnd={jest.fn()}
        loading={false}
      />
    );
  });

  it('mounts', () => {
    mount(globalViewer);
  });
});
