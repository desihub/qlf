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
      arms: 'r',
      desi_spectro_data: '/app/spectro/data',
      night: '20190101',
      exposures: '3,4',
      logpipeline: '/app/pipeline.log',
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
      arms: 'r',
      input: '/app/spectro/data',
      output: '/app/spectro/redux',
      exposures: '3,4',
      logfile: '/app/qlf.log',
      logpipeline: '/app/pipeline.log',
      loglevel: 'INFO',
      qlconfig:
        '/app/desispec/py/desispec/data/quicklook/qlconfig_darksurvey.yaml',
      spectrographs: '6,7'.split(','),
    });
  });

  it('changes night', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(0)
        .props().value
    ).toBe('20190101');
    await wrapper
      .find('input')
      .at(0)
      .simulate('change', { value: 'night' });
    expect(
      wrapper
        .find('TextField')
        .at(0)
        .props().value
    ).toBe('night');
  });

  it('changes exposure', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(1)
        .props().value
    ).toBe('3,4');
    await wrapper
      .find('input')
      .at(1)
      .simulate('change', { value: 'exp' });
    expect(
      wrapper
        .find('TextField')
        .at(1)
        .props().value
    ).toBe('exp');
  });

  it('changes input', async () => {
    expect(
      wrapper
        .find('input')
        .at(15)
        .props().value
    ).toBe('/app/spectro/data');
    await wrapper
      .find('input')
      .at(15)
      .simulate('change', { value: 'input' });
    expect(
      wrapper
        .find('TextField')
        .at(2)
        .props().value
    ).toBe('input');
  });

  it('changes output', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(3)
        .props().value
    ).toBe('/app/spectro/redux');
    await wrapper
      .find('input')
      .at(16)
      .simulate('change', { value: 'output' });
    expect(
      wrapper
        .find('TextField')
        .at(3)
        .props().value
    ).toBe('output');
  });

  it('changes loglevel', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(4)
        .props().value
    ).toBe('INFO');
    await wrapper
      .find('input')
      .at(17)
      .simulate('change', { value: 'DEBUG' });
    expect(
      wrapper
        .find('TextField')
        .at(4)
        .props().value
    ).toBe('DEBUG');
  });

  it('changes logfile', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(5)
        .props().value
    ).toBe('/app/qlf.log');
    await wrapper
      .find('input')
      .at(18)
      .simulate('change', { value: 'logfile' });
    expect(
      wrapper
        .find('TextField')
        .at(5)
        .props().value
    ).toBe('logfile');
  });

  it('changes logpipeline', async () => {
    expect(
      wrapper
        .find('TextField')
        .at(6)
        .props().value
    ).toBe('/app/pipeline.log');
    await wrapper
      .find('input')
      .at(19)
      .simulate('change', { value: 'pipeline' });
    expect(
      wrapper
        .find('TextField')
        .at(6)
        .props().value
    ).toBe('pipeline');
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
      .at(20)
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

  it('changes checked arm', async () => {
    expect(
      wrapper
        .find('input')
        .at(3)
        .props().checked
    ).toBe(true);
    await wrapper
      .find('input')
      .at(3)
      .simulate('change');
    expect(
      wrapper
        .find('input')
        .at(3)
        .props().checked
    ).toBe(false);
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
