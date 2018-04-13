import React, { Component } from 'react';
import ProcessingHistory from '../../screens/processing-history/processing-history';
import { Route } from 'react-router';
import Metrics from '../../screens/metrics/metrics';
import { connect } from 'react-redux';
import {
  getProcessingHistoryOrdered,
  getProcessingHistory,
  getQA,
  navigateToProcessingHistory,
  navigateToOfflineMetrics,
  navigateToOfflineQA,
} from './offline-store';
import PropTypes from 'prop-types';
import QA from '../../screens/qa/qa';
import _ from 'lodash';

const arms = ['b', 'r', 'z'];
const spectrographs = _.range(0, 9);

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
    navigateToProcessingHistory: PropTypes.func.isRequired,
    navigateToMetrics: PropTypes.func.isRequired,
    navigateToQA: PropTypes.func.isRequired,
  };

  navigateToQA = async processId => {
    this.props.navigateToQA();
    await this.props.getQA(processId);
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

  render() {
    return (
      <div>
        <Route
          path="/processing-history"
          render={() => (
            <ProcessingHistory
              getProcessingHistory={this.props.getProcessingHistory}
              getProcessingHistoryOrdered={
                this.props.getProcessingHistoryOrdered
              }
              processes={this.props.processes}
              navigateToQA={this.navigateToQA}
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
  }),
  dispatch => ({
    getProcessingHistoryOrdered: ordering =>
      dispatch(getProcessingHistoryOrdered(ordering)),
    getProcessingHistory: () => dispatch(getProcessingHistory()),
    getQA: processId => dispatch(getQA(processId)),
    navigateToProcessingHistory: () => dispatch(navigateToProcessingHistory()),
    navigateToMetrics: () => dispatch(navigateToOfflineMetrics()),
    navigateToQA: () => dispatch(navigateToOfflineQA()),
  })
)(OfflineContainer);
