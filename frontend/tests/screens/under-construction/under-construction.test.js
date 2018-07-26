import React from 'react';
import UnderConstruction from '../../../src/screens/under-construction/under-construction';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('UnderConstruction', () => {
  let underConstruction;
  beforeEach(() => {
    underConstruction = <UnderConstruction />;
  });

  it('mounts', () => {
    mount(underConstruction);
  });
});
