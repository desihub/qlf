import React from 'react';
import Stages from '../../../../../src/screens/monitor/widgets/stages/stages';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import sinon from 'sinon';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

configure({ adapter: new Adapter() });

const camera_stage = [
  {
    camera: [
      'processing_stage',
      'success_stage',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
    ],
  },
  {
    camera: [
      'none',
      'success_stage',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
    ],
  },
  {
    camera: [
      'none',
      'success_stage',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
    ],
  },
  {
    camera: [
      'none',
      'success_stage',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
      'none',
    ],
  },
];

describe('stages', () => {
  it('renders', () => {
    const openDialog = sinon.spy();
    const stages = (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <Stages status={camera_stage} arm={'z'} openDialog={openDialog} />
      </MuiThemeProvider>
    );
    mount(stages);
  });
});
