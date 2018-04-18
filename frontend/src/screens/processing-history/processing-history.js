import React, { Component } from 'react';
import Proptypes from 'prop-types';
import TableHistory from './widgets/table-history/table-history';
import SelectDate from './widgets/select-date/select-date';

export default class ProcessingHistory extends Component {
  static propTypes = {
    getProcessingHistory: Proptypes.func.isRequired,
    getProcessingHistoryOrdered: Proptypes.func.isRequired,
    navigateToQA: Proptypes.func.isRequired,
    processes: Proptypes.array.isRequired,
    startDate: Proptypes.string,
    endDate: Proptypes.string,
    getProcessingHistoryRangeDate: Proptypes.func.isRequired,
    lastProcess: Proptypes.number,
  };

  renderSelectDate = () => {
    if (this.props.startDate && this.props.endDate)
      return (
        <SelectDate
          startDate={this.props.startDate}
          endDate={this.props.endDate}
          getProcessingHistoryRangeDate={
            this.props.getProcessingHistoryRangeDate
          }
        />
      );
  };

  render() {
    return (
      <div>
        {this.renderSelectDate()}
        <TableHistory
          getProcessingHistory={this.props.getProcessingHistory}
          getProcessingHistoryOrdered={this.props.getProcessingHistoryOrdered}
          processes={this.props.processes}
          navigateToQA={this.props.navigateToQA}
          lastProcess={this.props.lastProcess}
        />
      </div>
    );
  }
}
