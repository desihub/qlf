import _ from 'lodash';
import { push } from 'react-router-redux';
import {
  fetchLastProcess,
  getHistoryDateRange,
} from '../offline/offline-store';
import bell from '../../assets/bell.mp3';

function defaultState() {
  return {
    daemonRunning: false,
    pipelineRunning: 'idle',
    mainTerminal: [],
    ingestionTerminal: [],
    cameraTerminal: [],
    camerasStages: { b: [], r: [], z: [] },
    qaTests: undefined,
    spectrographs: [],
    arms: [],
    mjd: '',
    date: '',
    time: '',
    processId: '',
    exposureId: '',
    flavor: '',
    arm: 0,
    spectrograph: 0,
    step: 0,
    notifications: [],
    online: undefined,
    websocketRef: undefined,
    soundActivated: true,
  };
}

function addNotification(state) {
  return { type: 'ADD_NOTIFICATION', state };
}

function setNotificationSound(soundActivated) {
  const state = { soundActivated };
  return { type: 'SET_NOTIFICATION_SOUND', state };
}

export function updateWebsocket(state) {
  return { type: 'UPDATE_WEBSOCKET_STATUS', state };
}

function updateMonitorState(state) {
  return { type: 'UPDATE_MONITOR_STATE', state };
}

export function updateCameraState(cameralog) {
  const state = { cameraTerminal: cameralog };
  return { type: 'UPDATE_CAMERA_STATE', state };
}

export function updateQA(state) {
  return { type: 'UPDATE_QA', state };
}

function selectMetric(step, spectrograph, arm) {
  const state = { step, spectrograph, arm };
  return { type: 'UPDATE_METRIC_SELECT_ONLINE', state };
}

export function updateLastProcessAndMonitor(state) {
  return async function(dispatch, getState) {
    if (
      getState().qlfOffline.recentProcesses &&
      state.processId !== '' &&
      !getState()
        .qlfOffline.recentProcesses.map(p => p.pk)
        .includes(parseInt(state.processId, 10))
    ) {
      await dispatch(getHistoryDateRange());
    }
    dispatch(fetchLastProcess());
    dispatch(updateMonitorState(state));
  };
}

export function navigateToOnlineMetrics(step, spectrograph, arm) {
  return function(dispatch) {
    dispatch(selectMetric(step, spectrograph, arm));
    dispatch(push('/metrics-realtime'));
  };
}

export function navigateToOnlineQA() {
  return function(dispatch) {
    dispatch(push('/qa-realtime'));
  };
}

export function setSound(soundActivated) {
  return function(dispatch) {
    dispatch(setNotificationSound(soundActivated));
  };
}

export function updateNotifications(notification) {
  return function(dispatch, getState) {
    const notifications = getState().qlfOnline.notifications.splice(0);
    notifications.unshift(notification);
    const sound = new Audio(bell);
    const { soundActivated } = getState().qlfOnline;
    if (
      process.env.REACT_APP_SOUND &&
      window.location.pathname === '/monitor-realtime' &&
      soundActivated
    )
      sound.play();
    dispatch(addNotification({ notifications }));
  };
}

export function clearNotifications() {
  return function(dispatch) {
    dispatch(addNotification({ notifications: [] }));
  };
}

function getUnique(availableCameras, index) {
  if (!availableCameras) return [];
  const arms = _.uniq(
    availableCameras.map(cam => {
      return cam[index];
    })
  );

  if (!index) {
    const orderedArms = [];
    if (arms.includes('b')) orderedArms.push('b');
    if (arms.includes('r')) orderedArms.push('r');
    if (arms.includes('z')) orderedArms.push('z');
    return orderedArms;
  }
  return arms;
}

export function qlfOnlineReducers(state = defaultState(), action) {
  switch (action.type) {
    case 'UPDATE_WEBSOCKET_STATUS':
      return Object.assign({}, state, {
        online: action.state.online,
      });
    case 'UPDATE_METRIC_SELECT_ONLINE':
      return Object.assign({}, state, {
        step: action.state.step,
        spectrograph: action.state.spectrograph,
        arm: action.state.arm,
      });
    case 'UPDATE_MONITOR_STATE':
      return Object.assign({}, state, {
        daemonRunning: action.state.daemonRunning,
        pipelineRunning: action.state.pipelineRunning,
        processId: action.state.processId,
        mainTerminal: action.state.mainTerminal,
        ingestionTerminal: action.state.ingestionTerminal,
        exposureId: action.state.exposureId,
        camerasStages: action.state.camerasStages,
        arms: getUnique(action.state.availableCameras, 0),
        spectrographs: getUnique(action.state.availableCameras, 1),
        mjd: action.state.mjd,
        date: action.state.date,
        time: action.state.time,
        flavor: action.state.flavor,
      });
    case 'UPDATE_QA':
      return Object.assign({}, state, {
        qaTests: action.state.qaTests,
      });
    case 'ADD_NOTIFICATION':
      return Object.assign({}, state, {
        notifications: action.state.notifications,
      });
    case 'UPDATE_CAMERA_STATE':
      if (action.state.cameraTerminal === 'Error') return state;
      return Object.assign({}, state, {
        cameraTerminal: action.state.cameraTerminal,
      });
    case 'SAVE_WEBSOCKET_REF':
      return Object.assign({}, state, {
        websocketRef: action.state.websocketRef,
      });
    case 'SET_NOTIFICATION_SOUND':
      return Object.assign({}, state, {
        soundActivated: action.state.soundActivated,
      });
    default:
      return state;
  }
}
