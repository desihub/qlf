import React from 'react';
import TrendAnalysis from '../../../src/screens/trend-analysis/trend-analysis';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('TrendAnalysis', () => {
  let trendAnalysis;
  beforeEach(() => {
    trendAnalysis = <TrendAnalysis />;
  });

  it('mounts', () => {
    mount(trendAnalysis);
  });
});
