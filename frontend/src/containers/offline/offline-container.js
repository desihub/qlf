import React, { Component } from 'react';
import History from '../../screens/history/history';
import { Route } from 'react-router';
import Configuration from '../../screens/configuration/configuration';
import Metrics from '../../screens/metrics/metrics';
import { connect } from 'react-redux';
import {
  getProcessingHistory,
  getObservingHistory,
  getQA,
  navigateToProcessingHistory,
  navigateToOfflineMetrics,
  getHistoryDateRange,
  navigateToOfflineQA,
  fetchLastProcess,
} from './offline-store';
import PropTypes from 'prop-types';
import QA from '../../screens/qa/qa';
import _ from 'lodash';
import { FadeLoader } from 'halogenium';
import UnderConstruction from '../../screens/under-construction/under-construction';
import CCDViewer from '../../screens/ccd-viewer/ccd-viewer';

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
    getObservingHistory: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    getQA: PropTypes.func.isRequired,
    pathname: PropTypes.string,
    exposureId: PropTypes.string.isRequired,
    qaTests: PropTypes.array.isRequired,
    mjd: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired,
    flavor: PropTypes.string.isRequired,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    navigateToProcessingHistory: PropTypes.func.isRequired,
    navigateToMetrics: PropTypes.func.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    arm: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired,
    spectrograph: PropTypes.number.isRequired,
    recentProcesses: PropTypes.array,
    recentExposures: PropTypes.array,
    processId: PropTypes.number,
    toggleHeader: PropTypes.func.isRequired,
    lastProcessedId: PropTypes.string,
    rowsCount: PropTypes.number,
    getHistoryDateRange: PropTypes.func,
    fetchLastProcess: PropTypes.func,
    daemonRunning: PropTypes.bool.isRequired,
    pipelineRunning: PropTypes.string.isRequired,
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
    this.props.getHistoryDateRange();
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
        <FadeLoader color="#424242" size="16px" margin="4px" />
      </div>
    );
  };

  navigateToCCD = (night, exposureId) => {
    window.open(
      `ccd-viewer?exposure=${exposureId}&night=${night}`,
      'ccd-viewer',
      'width=1050, height=850'
    );
  };

  render() {
    return (
      <div>
        {this.renderLoading()}
        <Route path="/ccd-viewer" render={() => <CCDViewer />} />
        <Route
          path="/afternoon-planning"
          render={() => (
            <History
              getHistory={this.props.getProcessingHistory}
              rows={this.props.rows}
              startDate={this.props.startDate}
              endDate={this.props.endDate}
              navigateToQA={this.navigateToQA}
              recentProcesses={this.props.recentProcesses}
              type={'process'}
              lastProcessedId={this.props.lastProcessedId}
              rowsCount={this.props.rowsCount}
              fetchLastProcess={this.props.fetchLastProcess}
              openCCDViewer={this.navigateToCCD}
            />
          )}
        />
        <Route
          path="/processing-history"
          render={() => (
            <History
              getHistory={this.props.getProcessingHistory}
              rows={this.props.rows}
              startDate={this.props.startDate}
              endDate={this.props.endDate}
              navigateToQA={this.navigateToQA}
              recentProcesses={this.props.recentProcesses}
              type={'process'}
              lastProcessedId={this.props.lastProcessedId}
              rowsCount={this.props.rowsCount}
              fetchLastProcess={this.props.fetchLastProcess}
              pipelineRunning={this.props.pipelineRunning}
              openCCDViewer={this.navigateToCCD}
            />
          )}
        />
        <Route
          path="/observing-history"
          render={() => (
            <History
              getHistory={this.props.getObservingHistory}
              rows={this.props.rows}
              startDate={this.props.startDate}
              endDate={this.props.endDate}
              navigateToQA={this.navigateToQA}
              recentExposures={this.props.recentExposures}
              type={'exposure'}
              lastProcessedId={this.props.lastProcessedId}
              rowsCount={this.props.rowsCount}
              fetchLastProcess={this.props.fetchLastProcess}
              openCCDViewer={this.navigateToCCD}
            />
          )}
        />
        <Route
          path="/qa"
          render={() => (
            <QA
              exposureId={this.props.exposureId}
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
              monitor={false}
              flavor={this.props.flavor}
            />
          )}
        />
        <Route
          path="/metrics"
          render={() => (
            <Metrics
              exposureId={this.props.exposureId}
              qaTests={this.props.qaTests}
              arms={arms}
              spectrographs={spectrographs}
              mjd={this.props.mjd}
              date={this.props.date}
              time={this.props.time}
              flavor={this.props.flavor}
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
        <Route
          path="/configuration"
          render={() => (
            <Configuration daemonRunning={this.props.daemonRunning} />
          )}
        />
        <Route
          path="/under-construction"
          render={() => <UnderConstruction />}
        />
      </div>
    );
  }
}

export default connect(
  state => ({
    rows: state.qlfOffline.rows,
    pathname: state.router.location ? state.router.location.pathname : null,
    exposureId: state.qlfOffline.exposureId,
    qaTests: state.qlfOffline.qaTests,
    mjd: state.qlfOffline.mjd,
    date: state.qlfOffline.date,
    time: state.qlfOffline.time,
    flavor: state.qlfOffline.flavor,
    arm: state.qlfOffline.arm,
    step: state.qlfOffline.step,
    spectrograph: state.qlfOffline.spectrograph,
    startDate: state.qlfOffline.startDate,
    endDate: state.qlfOffline.endDate,
    recentProcesses: state.qlfOffline.recentProcesses,
    recentExposures: state.qlfOffline.recentExposures,
    processId: state.qlfOffline.processId,
    lastProcessedId: state.qlfOnline.processId,
    rowsCount: state.qlfOffline.rowsCount,
    daemonRunning: state.qlfOnline.daemonRunning,
    pipelineRunning: state.qlfOnline.pipelineRunning,
  }),
  dispatch => ({
    getQA: processId => dispatch(getQA(processId)),
    navigateToProcessingHistory: () => dispatch(navigateToProcessingHistory()),
    navigateToMetrics: (step, spectrograph, arm) =>
      dispatch(navigateToOfflineMetrics(step, spectrograph, arm)),
    navigateToQA: () => dispatch(navigateToOfflineQA()),
    getProcessingHistory: (start, end, order, offset, limit, filters) =>
      dispatch(getProcessingHistory(start, end, order, offset, limit, filters)),
    getObservingHistory: (start, end, order, offset, limit, filters) =>
      dispatch(getObservingHistory(start, end, order, offset, limit, filters)),
    fetchLastProcess: () => dispatch(fetchLastProcess()),
    getHistoryDateRange: () => dispatch(getHistoryDateRange()),
  })
)(OfflineContainer);
