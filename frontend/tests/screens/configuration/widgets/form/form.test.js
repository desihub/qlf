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
      max_nights: '5',
      allowed_delay: '20',
      base_exposures_path: '/app/spectro/base_exposures',
      calibration_path: '/app/spectro/calibration',
    },
  };
  return {
    getCurrentConfiguration: jest.fn(() => qlfConfig),
    getDefaultConfiguration: jest.fn(() => qlfConfig),
    getCurrentThresholds: jest.fn(() => ({
      disk_percent_alert: '20',
      disk_percent_warning: '40',
    })),
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
  });

  // it('changes input', async () => {
  //   expect(
  //     wrapper
  //       .find('TextField')
  //       .at(1)
  //       .props().value
  //   ).toBe('/app/spectro/data');
  //   await wrapper
  //     .find('input')
  //     .at(8)
  //     .simulate('change', { target: { value: 'input' } });
  //   expect(
  //     wrapper
  //       .find('TextField')
  //       .at(5)
  //       .props().value
  //   ).toBe('input');
  // });

  // it('changes output', async () => {
  //   expect(
  //     wrapper
  //       .find('TextField')
  //       .at(6)
  //       .props().value
  //   ).toBe('/app/spectro/redux');
  //   await wrapper
  //     .find('input')
  //     .at(9)
  //     .simulate('change', { target: { value: 'output' } });
  //   expect(
  //     wrapper
  //       .find('TextField')
  //       .at(6)
  //       .props().value
  //   ).toBe('output');
  // });

  // it('changes calibration', async () => {
  //   expect(
  //     wrapper
  //       .find('TextField')
  //       .at(8)
  //       .props().value
  //   ).toBe('/app/spectro/calibration');
  //   await wrapper
  //     .find('input')
  //     .at(11)
  //     .simulate('change', { target: { value: 'calib' } });
  //   expect(
  //     wrapper
  //       .find('TextField')
  //       .at(8)
  //       .props().value
  //   ).toBe('calib');
  // });

  // it('changes checked arm and select all', async () => {
  //   expect(
  //     wrapper
  //       .find('path')
  //       .at(8)
  //       .props().style.fill
  //   ).toBe('green');
  //   expect(
  //     wrapper
  //       .find('input')
  //       .at(5)
  //       .props().checked
  //   ).toBe(true);
  //   await wrapper
  //     .find('input')
  //     .at(5)
  //     .simulate('change');
  //   expect(
  //     wrapper
  //       .find('path')
  //       .at(18)
  //       .props().style.fill
  //   ).toBe('lightgray');
  //   expect(
  //     wrapper
  //       .find('input')
  //       .at(5)
  //       .props().checked
  //   ).toBe(false);
  // });

  it('changes spectrograph selection', async () => {
    expect(
      wrapper
        .find('path')
        .at(23)
        .props().style.fill
    ).toBe('lightgray');
    wrapper
      .find('path')
      .at(23)
      .simulate('click');
    expect(
      wrapper
        .find('path')
        .at(23)
        .props().style.fill
    ).toBe('green');
  });

  it('clicks default button calls getDefaultConfiguration', async () => {
    expect(QlfApi.getDefaultConfiguration.mock.calls.length).toBe(0);
    await wrapper
      .find('Button')
      .at(1)
      .simulate('click');
    // expect(QlfApi.getDefaultConfiguration).toHaveBeenCalled();
  });
});
