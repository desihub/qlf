import React from 'react';
import Configuration from '../../../src/screens/configuration/configuration';
import { configure, mount } from 'enzyme';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

jest.mock('../../../src/containers/offline/connection/qlf-api', () => {
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
    getCurrentConfiguration: () => {
      return qlfConfig;
    },
    getDefaultConfiguration: () => {
      return qlfConfig;
    },
    getQlConfig: () => {
      return 'QLConfig';
    },
  };
});

describe('Configuration', () => {
  let wrapper;
  it('Mounts', async () => {
    const configuration = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Configuration />
      </MuiThemeProvider>
    );
    wrapper = await mount(configuration);
  });

  it('changes tab', async () => {
    await wrapper
      .find('Tab')
      .at(1)
      .simulate('click');
    expect(
      wrapper
        .find('Display')
        .at(0)
        .text()
    ).toBe('QLConfig');
  });
});
