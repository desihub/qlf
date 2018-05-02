import React, { Component } from 'react';
import History from '../../screens/history/history';
import { Route } from 'react-router';
import Metrics from '../../screens/metrics/metrics';
import { connect } from 'react-redux';
import {
  getProcessingHistoryOrdered,
  getProcessingHistory,
  getProcessingHistoryRangeDate,
  getObservingHistoryOrdered,
  getObservingHistory,
  getObservingHistoryRangeDate,
  getQA,
  navigateToProcessingHistory,
  navigateToOfflineMetrics,
  navigateToOfflineQA,
} from './offline-store';
import PropTypes from 'prop-types';
import QA from '../../screens/qa/qa';
import _ from 'lodash';
import { FadeLoader } from 'halogenium';

const arms = ['b', 'r', 'z'];
const spectrographs = _.range(0, 10);

const styles = {
  loading: {
    display: 'flex',
    position: 'fixed',
    width: '100%',
    height: '50%',
    justifyContent: 'center',
    alignItems: 'center',
  },
};

class OfflineContainer extends Component {
  static propTypes = {
    getProcessingHistory: PropTypes.func.isRequired,
    getProcessingHistoryOrdered: PropTypes.func.isRequired,
    getProcessingHistoryRangeDate: PropTypes.func.isRequired,
    getObservingHistory: PropTypes.func.isRequired,
    getObservingHistoryOrdered: PropTypes.func.isRequired,
    getObservingHistoryRangeDate: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    getQA: PropTypes.func.isRequired,
    pathname: PropTypes.string,
    exposure: PropTypes.string.isRequired,
    qaTests: PropTypes.array.isRequired,
    mjd: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func.isRequired,
    navigateToMetrics: PropTypes.func.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    arm: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired,
    spectrograph: PropTypes.number.isRequired,
    lastProcesses: PropTypes.array,
    processId: PropTypes.number,
    toggleHeader: PropTypes.func.isRequired,
    lastProcessedId: PropTypes.number,
  };

  state = {
    loading: false,
  };

  navigateToQA = async processId => {
    const urlProcessId = processId ? 'qa?process_id=' + processId : 'qa';
    window.open(urlProcessId, 'qa', 'width=850, height=650');
  };

  componentWillReceiveProps(nextProps) {
    if (
      nextProps.pathname &&
      this.props.pathname &&
      nextProps.pathname === '/processing-history' &&
      this.props.pathname !== '/processing-history'
    )
      this.props.getProcessingHistory();
  }

  searchQA = async processId => {
    this.setState({ loading: true });
    await this.props.getQA(processId);
    this.setState({ loading: false });
  };

  componentWillMount() {
    if (window.location.pathname === '/qa') {
      this.props.toggleHeader();
      if (window.location.search.includes('process_id=')) {
        const processId = window.location.search.split('process_id=')[1];
        this.searchQA(processId);
      }
    }
  }

  renderLoading = () => {
    if (!this.state.loading) return null;
    return (
      <div style={{ ...styles.loading }}>
        <FadeLoader color="teal" size="16px" margin="4px" />
      </div>
    );
  };

  render() {
    return (
      <div>
        {this.renderLoading()}
        <Route
          path="/processing-history"
          render={() => (
            <History
              getHistory={this.props.getProcessingHistory}
              getHistoryOrdered={this.props.getProcessingHistoryOrdered}
              rows={this.props.rows}
              startDate={this.props.startDate}
              endDate={this.props.endDate}
              navigateToQA={this.navigateToQA}
              getHistoryRangeDate={this.props.getProcessingHistoryRangeDate}
              lastProcesses={this.props.lastProcesses}
              type={'process'}
              lastProcessedId={this.props.lastProcessedId}
            />
          )}
        />
        <Route
          path="/observing-history"
          render={() => (
            <History
              getHistory={this.props.getObservingHistory}
              getHistoryOrdered={this.props.getObservingHistoryOrdered}
              rows={this.props.rows}
              startDate={this.props.startDate}
              endDate={this.props.endDate}
              navigateToQA={this.navigateToQA}
              getHistoryRangeDate={this.props.getObservingHistoryRangeDate}
              lastProcesses={this.props.lastProcesses}
              type={'exposure'}
              lastProcessedId={this.props.lastProcessedId}
            />
          )}
        />
        <Route
          path="/qa"
          render={() => (
            <QA
              exposure={this.props.exposure}
              qaTests={this.props.qaTests}
              arms={arms}
              spectrographs={spectrographs}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              navigateToProcessingHistory={
                this.props.navigateToProcessingHistory
              }
              navigateToMetrics={this.props.navigateToMetrics}
              petalSizeFactor={16}
              processId={this.props.processId}
            />
          )}
        />
        <Route
          path="/metrics"
          render={() => (
            <Metrics
              exposure={this.props.exposure}
              qaTests={this.props.qaTests}
              arms={arms}
              spectrographs={spectrographs}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              navigateToProcessingHistory={
                this.props.navigateToProcessingHistory
              }
              navigateToQA={this.props.navigateToQA}
              arm={this.props.arm}
              step={this.props.step}
              spectrograph={this.props.spectrograph}
              processId={this.props.processId}
            />
          )}
        />
      </div>
    );
  }
}

export default connect(
  state => ({
    rows: state.qlfOffline.rows,
    pathname: state.router.location ? state.router.location.pathname : null,
    exposure: state.qlfOffline.exposure,
    qaTests: state.qlfOffline.qaTests,
    mjd: state.qlfOffline.mjd,
    date: state.qlfOffline.date,
    time: state.qlfOffline.time,
    arm: state.qlfOffline.arm,
    step: state.qlfOffline.step,
    spectrograph: state.qlfOffline.spectrograph,
    startDate: state.qlfOffline.startDate,
    endDate: state.qlfOffline.endDate,
    lastProcesses: state.qlfOffline.lastProcesses,
    processId: state.qlfOffline.processId,
    lastProcessedId: state.qlfOnline.processId,
  }),
  dispatch => ({
    getQA: processId => dispatch(getQA(processId)),
    navigateToProcessingHistory: () => dispatch(navigateToProcessingHistory()),
    navigateToMetrics: (step, spectrograph, arm) =>
      dispatch(navigateToOfflineMetrics(step, spectrograph, arm)),
    navigateToQA: () => dispatch(navigateToOfflineQA()),
    getProcessingHistoryOrdered: ordering =>
      dispatch(getProcessingHistoryOrdered(ordering)),
    getProcessingHistory: () => dispatch(getProcessingHistory()),
    getProcessingHistoryRangeDate: (start, end) =>
      dispatch(getProcessingHistoryRangeDate(start, end)),
    getObservingHistoryOrdered: ordering =>
      dispatch(getObservingHistoryOrdered(ordering)),
    getObservingHistory: () => dispatch(getObservingHistory()),
    getObservingHistoryRangeDate: (start, end) =>
      dispatch(getObservingHistoryRangeDate(start, end)),
  })
)(OfflineContainer);
