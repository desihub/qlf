import React from 'react';
import Form from '../../../../../src/screens/configuration/widgets/form/form';
import { configure, mount } from 'enzyme';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import Adapter from 'enzyme-adapter-react-16';
import QlfApi from '../../../../../src/containers/offline/connection/qlf-api';

configure({ adapter: new Adapter() });

jest.mock('../../../../../src/containers/offline/connection/qlf-api', () => {
  const qlfConfig = {
    results: {
      logfile: '/app/qlf.log',
      desi_spectro_redux: '/app/spectro/redux',
      spectrographs: '7',
      qlconfig:
        '/app/desispec/py/desispec/data/quicklook/qlconfig_darksurvey.yaml',
      loglevel: 'INFO',
      arms: 'b,r',
      desi_spectro_data: '/app/spectro/data',
      night: '20190101',
      exposures: '3,4',
      logpipeline: '/app/pipeline.log',
      min_interval: '3',
      max_interval: '15',
      max_exposures: '10',
      allowed_delay: '20',
      base_exposures_path: '/app/spectro/base_exposures',
    },
  };
  return {
    getCurrentConfiguration: jest.fn(() => qlfConfig),
    getDefaultConfiguration: jest.fn(() => qlfConfig),
  };
});

describe('Configuration Form', () => {
  let wrapper;
  it('Mounts', async () => {
    const form = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Form />
      </MuiThemeProvider>
    );
    wrapper = await mount(form);
    wrapper.setState({
      night: '20190101',
      arms: 'b,r',
      input: '/app/spectro/data',
      output: '/app/spectro/redux',
      exposures: '3,4',
      minInterval: '3',
      maxInterval: '15',
      maxExposures: '10',
      allowedDelay: '20',
      baseExposures: '/app/spectro/base_exposures',
      qlconfig:
        '/app/desispec/py/desispec/data/quicklook/qlconfig_darksurvey.yaml',
      spectrographs: 'r0,b0'.split(','),
    });
  });

  it('changes minInterval', async () => {
    expect(
      wrapper
        .find('input')
        .at(0)
        .props().value
    ).toBe('3');
    await wrapper
      .find('input')
      .at(0)
      .simulate('change', { value: 'minInterval' });
    expect(
      wrapper
        .find('TextField')
        .at(0)
        .props().value
    ).toBe('minInterval');
  });

  it('changes maxInterval', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(1)
        .props().value
    ).toBe('15');
    await wrapper
      .find('input')
      .at(1)
      .simulate('change', { value: 'maxInterval' });
    expect(
      wrapper
        .find('TextField')
        .at(1)
        .props().value
    ).toBe('maxInterval');
  });

  it('changes delay', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(2)
        .props().value
    ).toBe('20');
    await wrapper
      .find('input')
      .at(2)
      .simulate('change', { value: 'delay' });
    expect(
      wrapper
        .find('TextField')
        .at(2)
        .props().value
    ).toBe('delay');
  });

  it('changes maxExposures', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(3)
        .props().value
    ).toBe('10');
    await wrapper
      .find('input')
      .at(3)
      .simulate('change', { value: 'maxExposures' });
    expect(
      wrapper
        .find('TextField')
        .at(3)
        .props().value
    ).toBe('maxExposures');
  });

  it('changes input', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(4)
        .props().value
    ).toBe('/app/spectro/data');
    await wrapper
      .find('input')
      .at(37)
      .simulate('change', { value: 'input' });
    expect(
      wrapper
        .find('TextField')
        .at(4)
        .props().value
    ).toBe('input');
  });

  it('changes output', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(5)
        .props().value
    ).toBe('/app/spectro/redux');
    await wrapper
      .find('input')
      .at(38)
      .simulate('change', { value: 'output' });
    expect(
      wrapper
        .find('TextField')
        .at(5)
        .props().value
    ).toBe('output');
  });

  it('changes baseExposures', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(6)
        .props().value
    ).toBe('/app/spectro/base_exposures');
    await wrapper
      .find('input')
      .at(39)
      .simulate('change', { value: 'baseExposures' });
    expect(
      wrapper
        .find('TextField')
        .at(6)
        .props().value
    ).toBe('baseExposures');
  });

  it('changes qlconfig', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(7)
        .props().value
    ).toBe('/app/desispec/py/desispec/data/quicklook/qlconfig_darksurvey.yaml');
    await wrapper
      .find('input')
      .at(40)
      .simulate('change', { value: 'qlconfig' });
    expect(
      wrapper
        .find('TextField')
        .at(7)
        .props().value
    ).toBe('qlconfig');
  });

  it('changes checked spectrograph', async () => {
    expect(
      wrapper
        .find('input')
        .at(7)
        .props().checked
    ).toBe(false);
    await wrapper
      .find('input')
      .at(7)
      .simulate('change');
    expect(
      wrapper
        .find('input')
        .at(7)
        .props().checked
    ).toBe(true);
  });

  it('changes checked arm and select all', async () => {
    expect(
      wrapper
        .find('input')
        .at(4)
        .props().checked
    ).toBe(true);
    await wrapper
      .find('input')
      .at(4)
      .simulate('change');
    expect(
      wrapper
        .find('input')
        .at(4)
        .props().checked
    ).toBe(false);
    expect(
      wrapper
        .find('input')
        .at(8)
        .props().checked
    ).toBe(false);
    await wrapper
      .find('input')
      .at(4)
      .simulate('change');
    expect(
      wrapper
        .find('input')
        .at(8)
        .props().checked
    ).toBe(true);
  });

  it('clicks default button calls getDefaultConfiguration', async () => {
    expect(QlfApi.getDefaultConfiguration.mock.calls.length).toBe(0);
    await wrapper
      .find('Button')
      .at(1)
      .simulate('click');
    expect(QlfApi.getDefaultConfiguration).toHaveBeenCalled();
  });
});
