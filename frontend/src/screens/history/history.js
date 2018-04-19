import React, { Component } from 'react';
import Proptypes from 'prop-types';
import TableHistory from './widgets/table-history/table-history';
import SelectDate from './widgets/select-date/select-date';

export default class History extends Component {
  static propTypes = {
    getHistory: Proptypes.func.isRequired,
    getHistoryOrdered: Proptypes.func.isRequired,
    navigateToQA: Proptypes.func.isRequired,
    processes: Proptypes.array.isRequired,
    startDate: Proptypes.string,
    endDate: Proptypes.string,
    getHistoryRangeDate: Proptypes.func.isRequired,
    lastProcess: Proptypes.number,
  };

  renderSelectDate = () => {
    if (this.props.startDate && this.props.endDate)
      return (
        <SelectDate
          startDate={this.props.startDate}
          endDate={this.props.endDate}
          getHistoryRangeDate={this.props.getHistoryRangeDate}
        />
      );
  };

  render() {
    return (
      <div>
        {this.renderSelectDate()}
        <TableHistory
          getHistory={this.props.getHistory}
          getHistoryOrdered={this.props.getHistoryOrdered}
          processes={this.props.processes}
          navigateToQA={this.props.navigateToQA}
          lastProcess={this.props.lastProcess}
        />
      </div>
    );
  }
}
