import React, { Component } from 'react';
import History from '../../screens/history/history';
import { Route } from 'react-router';
import Metrics from '../../screens/metrics/metrics';
import { connect } from 'react-redux';
import {
  getProcessingHistoryOrdered,
  getProcessingHistory,
  getProcessingHistoryRangeDate,
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
const spectrographs = _.range(0, 9);

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
    processes: PropTypes.array.isRequired,
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
    getProcessingHistoryRangeDate: PropTypes.func.isRequired,
    lastProcess: PropTypes.number,
  };

  state = {
    loading: false,
  };

  navigateToQA = async processId => {
    this.setState({ loading: true });
    this.props.navigateToQA();
    await this.props.getQA(processId);
    this.setState({ loading: false });
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
              processes={this.props.processes}
              startDate={this.props.startDate}
              endDate={this.props.endDate}
              navigateToQA={this.navigateToQA}
              getHistoryRangeDate={this.props.getProcessingHistoryRangeDate}
              lastProcess={this.props.lastProcess}
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
            />
          )}
        />
      </div>
    );
  }
}

export default connect(
  state => ({
    processes: state.qlfOffline.processes,
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
    lastProcess: state.qlfOffline.lastProcess,
  }),
  dispatch => ({
    getProcessingHistoryOrdered: ordering =>
      dispatch(getProcessingHistoryOrdered(ordering)),
    getProcessingHistory: () => dispatch(getProcessingHistory()),
    getQA: processId => dispatch(getQA(processId)),
    navigateToProcessingHistory: () => dispatch(navigateToProcessingHistory()),
    navigateToMetrics: (step, spectrograph, arm) =>
      dispatch(navigateToOfflineMetrics(step, spectrograph, arm)),
    navigateToQA: () => dispatch(navigateToOfflineQA()),
    getProcessingHistoryRangeDate: (start, end) =>
      dispatch(getProcessingHistoryRangeDate(start, end)),
  })
)(OfflineContainer);
