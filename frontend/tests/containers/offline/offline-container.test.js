import React from 'react';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { store } from '../../../src/store';
import { Provider } from 'react-redux';
import OfflineContainer from '../../../src/containers/offline/offline-container';
import { BrowserRouter as Router } from 'react-router-dom';
import { LOCATION_CHANGE } from 'react-router-redux';

configure({ adapter: new Adapter() });

jest.mock('../../../src/containers/offline/connection/qlf-api', () => {
  return {
    getLastProcess: () => {
      return [{ id: 69 }];
    },
    getProcessingHistory: () => {
      return {
        results: {
          results: [
            {
              pk: 69,
              dateobs: '2019-01-01T22:00:00Z',
              datemjd: 58484.916666666664,
              exposure_id: 3,
              tile: 6,
              telra: 333.22,
              teldec: 14.84,
              exptime: 1000,
              airmass: null,
              runtime: '110.648429',
            },
            {
              pk: 70,
              dateobs: '2019-01-01T22:00:00Z',
              datemjd: 58484.916666666664,
              exposure_id: 4,
              tile: 7,
              telra: 332.35,
              teldec: 12.32,
              exptime: 1000,
              airmass: null,
              runtime: '96.254038',
            },
          ],
        },
      };
    },
  };
});

describe('OfflineContainer', () => {
  let offline;
  it('renders without crashing', () => {
    offline = (
      <Provider store={store}>
        <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
          <Router>
            <OfflineContainer />
          </Router>
        </MuiThemeProvider>
      </Provider>
    );
    store.dispatch({
      type: LOCATION_CHANGE,
      payload: {
        pathname: '/',
      },
    });
  });

  it('navigates to process-history', async () => {
    mount(offline);
    await store.dispatch({
      type: LOCATION_CHANGE,
      payload: {
        pathname: '/processing-history',
      },
    });
    expect(store.getState().router.location.pathname).toBe(
      '/processing-history'
    );
    await mount(offline);
    expect(store.getState().qlfOffline.rows).toEqual([
      {
        pk: 69,
        dateobs: '2019-01-01T22:00:00Z',
        datemjd: 58484.916666666664,
        exposure_id: 3,
        tile: 6,
        telra: 333.22,
        teldec: 14.84,
        exptime: 1000,
        airmass: null,
        runtime: '110.648429',
      },
      {
        pk: 70,
        dateobs: '2019-01-01T22:00:00Z',
        datemjd: 58484.916666666664,
        exposure_id: 4,
        tile: 7,
        telra: 332.35,
        teldec: 12.32,
        exptime: 1000,
        airmass: null,
        runtime: '96.254038',
      },
    ]);
  });
});
