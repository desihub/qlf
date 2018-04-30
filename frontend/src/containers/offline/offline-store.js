import QlfApi from './connection/qlf-api';
import { push } from 'react-router-redux';

function defaultState() {
  return {
    rows: [],
    mjd: '',
    date: '',
    time: '',
    exposure: '',
    processId: undefined,
    lastProcesses: undefined,
    qaTests: [],
    arm: 0,
    spectrograph: 0,
    step: 0,
    startDate: undefined,
    endDate: undefined,
  };
}

function updateRows(rows) {
  const state = { rows };
  return { type: 'UPDATE_ROWS', state };
}

function updateDateRange(startDate, endDate) {
  const state = { startDate, endDate };
  return { type: 'UPDATE_DATE_RANGE', state };
}

function updateLastProcess(lastProcesses) {
  const state = { lastProcesses };
  return { type: 'UPDATE_LAST_PROCESSES', state };
}

export function fetchLastProcess() {
  return async function(dispatch) {
    const lastProcesses = await QlfApi.getProcessingHistoryLimit();
    if (lastProcesses && !lastProcesses.detail && lastProcesses.results)
      dispatch(updateLastProcess(lastProcesses.results));
  };
}

function updateQA(qaTests) {
  const state = {
    mjd: qaTests.datemjd.toFixed(5),
    qaTests: qaTests.qa_tests,
    date: qaTests.date.split('T')[0],
    time: qaTests.date.split('T')[1],
    processId: qaTests.pk,
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
    const rows = await QlfApi.getProcessingHistory();
    const dateRange = await QlfApi.getExposuresDateRange();
    if (rows && rows.results) {
      dispatch(updateRows(rows.results));
    }

    if (dateRange && dateRange.end_date && dateRange.start_date) {
      dispatch(updateDateRange(dateRange.start_date, dateRange.end_date));
    }
  };
}

export function getProcessingHistoryRangeDate(start, end) {
  return async function(dispatch) {
    const rows = await QlfApi.getProcessingHistoryRangeDate(
      start.toISOString().split('T')[0],
      end.toISOString().split('T')[0]
    );

    if (rows && rows.results) {
      await dispatch(updateRows(rows.results));
    }
  };
}

export function getProcessingHistoryOrdered(ordering) {
  return async function(dispatch) {
    const rows = await QlfApi.getProcessingHistoryOrdered(ordering);
    if (rows && rows.results) await dispatch(updateRows(rows.results));
  };
}

export function getObservingHistory() {
  return async function(dispatch) {
    const rows = await QlfApi.getObservingHistory();
    const dateRange = await QlfApi.getExposuresDateRange();
    if (rows && rows.results) {
      dispatch(updateRows(rows.results));
    }

    if (dateRange && dateRange.end_date && dateRange.start_date) {
      dispatch(updateDateRange(dateRange.start_date, dateRange.end_date));
    }
  };
}

export function getObservingHistoryRangeDate(start, end) {
  return async function(dispatch) {
    const rows = await QlfApi.getObservingHistoryRangeDate(
      start.toISOString().split('T')[0],
      end.toISOString().split('T')[0]
    );

    if (rows && rows.results && rows.results) {
      await dispatch(updateRows(rows.results));
    }
  };
}

export function getObservingHistoryOrdered(ordering) {
  return async function(dispatch) {
    const rows = await QlfApi.getObservingHistoryOrdered(ordering);
    if (rows && rows.results && rows.results)
      await dispatch(updateRows(rows.results));
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
    case 'UPDATE_LAST_PROCESSES':
      return Object.assign({}, state, {
        lastProcesses: action.state.lastProcesses,
      });
    case 'UPDATE_DATE_RANGE':
      return Object.assign({}, state, {
        startDate: action.state.startDate,
        endDate: action.state.endDate,
      });
    case 'UPDATE_ROWS':
      return Object.assign({}, state, {
        rows: action.state.rows,
      });
    case 'UPDATE_OFFLINE_QA':
      return Object.assign({}, state, {
        mjd: action.state.mjd,
        date: action.state.date,
        time: action.state.time,
        processId: action.state.processId,
        qaTests: action.state.qaTests,
        exposure: action.state.exposure,
      });
    default:
      return state;
  }
}
