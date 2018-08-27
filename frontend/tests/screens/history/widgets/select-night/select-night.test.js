import React from 'react';
import SelectNight from '../../../../../src/screens/history/widgets/select-night/select-night';
import { mount, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('SelectNight', () => {
  let selectNight;
  beforeEach(() => {
    selectNight = <SelectNight />;
  });

  it('mounts', () => {
    mount(selectNight);
  });
});
