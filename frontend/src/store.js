import { createStore, combineReducers, applyMiddleware } from 'redux';
import { routerReducer, routerMiddleware } from 'react-router-redux';
import createHistory from 'history/createBrowserHistory';
import thunk from 'redux-thunk';
import { qlfOnlineReducers } from './containers/online/online-store';
import { qlfOfflineReducers } from './containers/offline/offline-store';

export const history = createHistory();
const router = routerMiddleware(history);

export const store = createStore(
  combineReducers({
    qlfOnline: qlfOnlineReducers,
    qlfOffline: qlfOfflineReducers,
    router: routerReducer,
  }),
  applyMiddleware(router, thunk)
);
