import React from 'react';
import TrendViewer from '../../../../src/screens/trend-analysis/trend-viewer/trend-viewer';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('TrendViewer', () => {
  let trendViewer;
  beforeEach(() => {
    trendViewer = <TrendViewer startDate={jest.string} endDate={jest.string} />;
  });

  it('mounts', () => {
    mount(trendViewer);
  });
});
