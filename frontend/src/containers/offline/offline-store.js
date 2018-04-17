import QlfApi from './connection/qlf-api';
import { push } from 'react-router-redux';

function defaultState() {
  return {
    processes: [],
    mjd: '',
    date: '',
    time: '',
    exposure: '',
    qaTests: [],
  };
}

function updateProcesses(processes) {
  const state = { processes };
  return { type: 'UPDATE_PROCESSES', state };
}

function updateQA(qaTests) {
  const state = {
    mjd: qaTests.datemjd.toFixed(5),
    qaTests: qaTests.qa_tests,
    date: qaTests.date.split('T')[0],
    time: qaTests.date.split('T')[1],
    exposure: qaTests.exposure_id.toString(),
  };
  return { type: 'UPDATE_OFFLINE_QA', state };
}

export function getProcessingHistory() {
  return async function(dispatch) {
    const processes = await QlfApi.getProcessingHistory();
    if (processes) await dispatch(updateProcesses(processes.results));
  };
}

export function getProcessingHistoryOrdered(ordering) {
  return async function(dispatch) {
    const processes = await QlfApi.getProcessingHistoryOrdered(ordering);
    if (processes) dispatch(updateProcesses(processes.results));
  };
}

export function getQA(processId) {
  return async function(dispatch) {
    const qa = await QlfApi.getQA(processId);
    await dispatch(updateQA(qa));
  };
}

export function navigateToProcessingHistory() {
  return async function(dispatch) {
    dispatch(push('/processing-history'));
  };
}

export function navigateToOfflineMetrics() {
  return function(dispatch) {
    dispatch(push('/metrics'));
  };
}

export function navigateToOfflineQA() {
  return function(dispatch) {
    dispatch(push('/qa'));
  };
}

export function qlfOfflineReducers(state = defaultState(), action) {
  switch (action.type) {
    case 'UPDATE_PROCESSES':
      return Object.assign({}, state, {
        processes: action.state.processes,
      });
    case 'UPDATE_OFFLINE_QA':
      return Object.assign({}, state, {
        mjd: action.state.mjd,
        date: action.state.date,
        time: action.state.time,
        qaTests: action.state.qaTests,
        exposure: action.state.exposure,
      });
    default:
      return state;
  }
}
