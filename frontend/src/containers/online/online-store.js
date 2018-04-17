import _ from 'lodash';
import { push } from 'react-router-redux';

function defaultState() {
  return {
    daemonStatus: 'idle',
    exposure: 'none',
    mainTerminal: [],
    ingestionTerminal: [],
    cameraTerminal: [],
    camerasStages: { b: [], r: [], z: [] },
    qaTests: [],
    spectrographs: [],
    arms: [],
    mjd: '',
    date: '',
    time: '',
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

export function navigateToOnlineMetrics() {
  return function(dispatch) {
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
    case 'UPDATE_MONITOR_STATE':
      return Object.assign({}, state, {
        daemonStatus: action.state.daemonStatus,
        mainTerminal: action.state.mainTerminal,
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
