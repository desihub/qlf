import _ from 'lodash';
import { push } from 'react-router-redux';

function defaultState() {
  return {
    daemonStatus: 'idle',
    exposure: 'none',
    ingestionTerminal: [],
    cameraTerminal: [],
    camerasStages: { b: [], r: [], z: [] },
    qaTests: [],
    spectrographs: [],
    arms: [],
    mjd: '',
    date: '',
    time: '',
    processId: undefined,
    arm: 0,
    spectrograph: 0,
    step: 0,
  };
}

export function updateMonitorState(state) {
  return { type: 'UPDATE_MONITOR_STATE', state };
}

export function updateCameraState(state) {
  return { type: 'UPDATE_CAMERA_STATE', state };
}

export function updateQA(state) {
  return { type: 'UPDATE_QA', state };
}

function selectMetric(step, spectrograph, arm) {
  const state = { step, spectrograph, arm };
  return { type: 'UPDATE_METRIC_SELECT_ONLINE', state };
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
    case 'UPDATE_METRIC_SELECT_ONLINE':
      return Object.assign({}, state, {
        step: action.state.step,
        spectrograph: action.state.spectrograph,
        arm: action.state.arm,
      });
    case 'UPDATE_MONITOR_STATE':
      return Object.assign({}, state, {
        daemonStatus: action.state.daemonStatus,
        processId: action.state.processId,
        ingestionTerminal: action.state.ingestionTerminal,
        exposure: action.state.exposure,
        camerasStages: action.state.camerasStages,
        arms: getUnique(action.state.availableCameras, 0),
        spectrographs: getUnique(action.state.availableCameras, 1),
        mjd: action.state.mjd,
        date: action.state.date,
        time: action.state.time,
      });
    case 'UPDATE_QA':
      return Object.assign({}, state, {
        qaTests: action.state.qaTests,
      });
    case 'UPDATE_CAMERA_STATE':
      if (action.state.cameraTerminal === 'Error') return state;
      return Object.assign({}, state, {
        cameraTerminal: action.state.cameraTerminal,
      });
    default:
      return state;
  }
}
