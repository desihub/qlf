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
    arm: 0,
    spectrograph: 0,
    step: 0,
  };
}

function updateProcesses(processes) {
  const state = { processes };
  return { type: 'UPDATE_PROCESSES', state };
}

function updateDateRange(startDate, endDate) {
  const state = { startDate, endDate };
  return { type: 'UPDATE_DATE_RANGE', state };
}

function updateLastProcess(lastProcess) {
  const state = { lastProcess };
  return { type: 'UPDATE_LAST_PROCESS', state };
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

function selectMetric(step, spectrograph, arm) {
  const state = { step, spectrograph, arm };
  return { type: 'UPDATE_METRIC_SELECT_OFFLINE', state };
}

export function getProcessingHistory() {
  return async function(dispatch) {
    const processes = await QlfApi.getProcessingHistory();
    const lastProcess = await QlfApi.getLastProcess();
    if (processes && processes.results && processes.results.results) {
      dispatch(updateProcesses(processes.results.results));
    }

    if (
      processes &&
      processes.results &&
      processes.results.start_date &&
      processes.results.end_date
    ) {
      dispatch(
        updateDateRange(
          processes.results.start_date,
          processes.results.end_date
        )
      );
    }

    if (lastProcess[0] && lastProcess[0].id) {
      dispatch(updateLastProcess(lastProcess[0].id));
    }
  };
}

export function getProcessingHistoryRangeDate(start, end) {
  return async function(dispatch) {
    const processes = await QlfApi.getProcessingHistoryRangeDate(
      start.toISOString().split('T')[0],
      end.toISOString().split('T')[0]
    );
    if (processes) {
      await dispatch(updateProcesses(processes));
    }
  };
}

export function getProcessingHistoryOrdered(ordering) {
  return async function(dispatch) {
    const processes = await QlfApi.getProcessingHistoryOrdered(ordering);
    if (processes && processes.results && processes.results.results)
      await dispatch(updateProcesses(processes.results.results));
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

export function navigateToOfflineMetrics(step, spectrograph, arm) {
  return function(dispatch) {
    dispatch(selectMetric(step, spectrograph, arm));
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
    case 'UPDATE_METRIC_SELECT_OFFLINE':
      return Object.assign({}, state, {
        step: action.state.step,
        spectrograph: action.state.spectrograph,
        arm: action.state.arm,
      });
    case 'UPDATE_LAST_PROCESS':
      return Object.assign({}, state, {
        lastProcess: action.state.lastProcess,
      });
    case 'UPDATE_DATE_RANGE':
      return Object.assign({}, state, {
        startDate: action.state.startDate,
        endDate: action.state.endDate,
      });
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
