import React, { Component } from 'react';
import Proptypes from 'prop-types';
import TableHistory from './widgets/table-history/table-history';

export default class ProcessingHistory extends Component {
  static propTypes = {
    getProcessingHistory: Proptypes.func.isRequired,
    getProcessingHistoryOrdered: Proptypes.func.isRequired,
    navigateToQA: Proptypes.func.isRequired,
    processes: Proptypes.array.isRequired,
  };

  render() {
    return (
      <TableHistory
        getProcessingHistory={this.props.getProcessingHistory}
        getProcessingHistoryOrdered={this.props.getProcessingHistoryOrdered}
        processes={this.props.processes}
        navigateToQA={this.props.navigateToQA}
      />
    );
  }
}
