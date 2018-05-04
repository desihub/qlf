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
    startDate: '',
    endDate: '',
    rowsCount: undefined,
  };
}

function updateRows(rows) {
  const state = { rows };
  return { type: 'UPDATE_ROWS', state };
}

function updateRowsCount(count) {
  const state = { count };
  return { type: 'UPDATE_ROWS_COUNT', state };
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
  return async function(dispatch, getState) {
    const { startDate, endDate } = getState().qlfOffline;
    const lastProcesses = await QlfApi.getProcessingHistory(
      startDate,
      endDate,
      '-pk',
      0,
      10
    );
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

export function getHistoryDateRange() {
  return async function(dispatch) {
    const dateRange = await QlfApi.getExposuresDateRange();
    if (dateRange && dateRange.end_date && dateRange.start_date) {
      dispatch(updateDateRange(dateRange.start_date, dateRange.end_date));
    }
  };
}

export function getProcessingHistory(start, end, order, offset, limit) {
  return async function(dispatch) {
    const rows = await QlfApi.getProcessingHistory(
      start,
      end,
      order,
      offset,
      limit
    );
    if (rows && rows.results) {
      dispatch(updateRowsCount(rows.count));
      dispatch(updateRows(rows.results));
    }
  };
}

export function getObservingHistory(start, end, order, offset, limit) {
  return async function(dispatch) {
    const rows = await QlfApi.getObservingHistory(
      start,
      end,
      order,
      offset,
      limit
    );
    if (rows && rows.results) {
      dispatch(updateRowsCount(rows.count));
      dispatch(updateRows(rows.results));
    }
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
    case 'UPDATE_ROWS_COUNT':
      return Object.assign({}, state, {
        rowsCount: action.state.count,
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
