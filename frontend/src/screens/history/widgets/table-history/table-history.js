import React, { Component } from 'react';
import { Table, TableBody } from 'material-ui/Table';
import PropTypes from 'prop-types';
import HistoryHeader from './history-header/history-header';
import HistoryData from './history-data/history-data';

export default class TableHistory extends Component {
  static propTypes = {
    getHistory: PropTypes.func.isRequired,
    getHistoryOrdered: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    onRowSelection: PropTypes.func,
    type: PropTypes.string.isRequired,
    selectable: PropTypes.bool,
    orderable: PropTypes.bool,
    processId: PropTypes.number,
    lastProcessedId: PropTypes.number,
    selectedExposures: PropTypes.array,
  };

  state = {
    rows: undefined,
    asc: undefined,
    ordering: undefined,
  };

  componentWillMount() {
    this.props.getHistory();
  }

  getHistoryOrdered = async ordering => {
    const order = this.state.asc ? ordering : `-${ordering}`;
    this.setState({
      rows: await this.props.getHistoryOrdered(order),
      asc: !this.state.asc,
      ordering,
    });
  };

  selectProcessQA = pk => {
    this.props.navigateToQA(pk);
  };

  renderBody = () => {
    const isProcessHistory = this.props.type === 'process';
    return (
      <TableBody
        showRowHover={true}
        displayRowCheckbox={!isProcessHistory && this.props.selectable}
      >
        {this.props.rows.map((row, id) => {
          const processId =
            isProcessHistory || !row.last_exposure_process_id
              ? row.pk
              : row.last_exposure_process_id;
          return (
            <HistoryData
              key={id}
              processId={processId}
              row={row}
              selectProcessQA={this.selectProcessQA}
              type={this.props.type}
              lastProcessedId={this.props.lastProcessedId}
              selectedExposures={this.props.selectedExposures}
            />
          );
        })}
      </TableBody>
    );
  };

  render() {
    const isProcessHistory = this.props.type === 'process';
    return (
      <div>
        <Table
          fixedHeader={false}
          style={{ width: 'auto', tableLayout: 'auto' }}
          bodyStyle={{ overflow: 'visible' }}
          selectable={!isProcessHistory && this.props.selectable}
          multiSelectable={true}
          onRowSelection={this.props.onRowSelection}
        >
          <HistoryHeader
            getHistoryOrdered={this.getHistoryOrdered}
            type={this.props.type}
            asc={this.state.asc}
            ordering={this.state.ordering}
            selectable={this.props.selectable}
            orderable={this.props.orderable}
          />
          {this.renderBody()}
        </Table>
      </div>
    );
  }
}
