import React, { Component } from 'react';
import PropTypes from 'prop-types';
import HistoryHeader from './history-header/history-header';
import HistoryData from './history-data/history-data';
import { withStyles } from 'material-ui-next/styles';
import Table, { TableBody, TablePagination } from 'material-ui-next/Table';

class TableHistory extends Component {
  static propTypes = {
    getHistory: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    selectExposure: PropTypes.func,
    type: PropTypes.string.isRequired,
    selectable: PropTypes.bool,
    orderable: PropTypes.bool,
    processId: PropTypes.number,
    lastProcessedId: PropTypes.number,
    selectedExposures: PropTypes.array,
    rowsCount: PropTypes.number,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    classes: PropTypes.object.isRequired,
    changeLimit: PropTypes.func.isRequired,
    limit: PropTypes.number.isRequired,
  };

  state = {
    asc: undefined,
    ordering: '-pk',
    offset: 0,
    filters: '',
  };

  componentWillReceiveProps(nextProps) {
    if (
      nextProps.startDate &&
      nextProps.endDate &&
      this.props.endDate !== nextProps.endDate
    ) {
      this.props.getHistory(
        nextProps.startDate,
        nextProps.endDate,
        this.state.ordering,
        this.state.offset,
        this.props.limit,
        this.state.filters
      );
    }
  }

  selectProcessQA = pk => {
    this.props.navigateToQA(pk);
  };

  renderBody = () => {
    const isProcessHistory = this.props.type === 'process';
    return (
      <TableBody>
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
              rowNumber={id}
              selectProcessQA={this.selectProcessQA}
              type={this.props.type}
              lastProcessedId={this.props.lastProcessedId}
              selectedExposures={this.props.selectedExposures}
              selectExposure={this.props.selectExposure}
              selectable={this.props.selectable}
            />
          );
        })}
      </TableBody>
    );
  };

  addOrder = ordering => {
    const order = this.state.asc ? ordering : `-${ordering}`;
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      order,
      this.state.offset,
      this.props.limit,
      this.state.filters
    );
    this.setState({
      asc: !this.state.asc,
      ordering,
      offset: 0,
    });
  };

  addFilters = filters => {
    this.setState({ filters });
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      this.state.ordering,
      this.state.offset,
      this.props.limit,
      filters
    );
  };

  handleChangePage = (evt, offset) => {
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      this.state.ordering,
      offset * this.props.limit,
      this.props.limit,
      this.state.filters
    );
    this.setState({ offset });
  };

  handleChangeRowsPerPage = event => {
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      this.state.ordering,
      this.state.offset * this.props.limit,
      event.target.value,
      this.state.filters
    );
    this.props.changeLimit(event.target.value);
  };

  renderPagination = () => {
    if (!this.props.rowsCount) return;
    return (
      <TablePagination
        component="div"
        count={this.props.rowsCount}
        rowsPerPage={this.props.limit}
        page={this.state.offset}
        backIconButtonProps={{
          'aria-label': 'Previous Page',
        }}
        nextIconButtonProps={{
          'aria-label': 'Next Page',
        }}
        onChangePage={this.handleChangePage}
        onChangeRowsPerPage={this.handleChangeRowsPerPage}
      />
    );
  };

  render() {
    return (
      <div className={this.props.classes.root}>
        <Table style={{ width: 'auto', tableLayout: 'auto' }}>
          <HistoryHeader
            addOrder={this.addOrder}
            addFilters={this.addFilters}
            type={this.props.type}
            asc={this.state.asc}
            ordering={this.state.ordering}
            selectable={this.props.selectable}
            orderable={this.props.orderable}
            selectExposure={this.props.selectExposure}
          />
          {this.renderBody()}
        </Table>
        {this.renderPagination()}
      </div>
    );
  }
}

const styles = {
  root: {
    width: '100%',
    overflowX: 'auto',
  },
};

export default withStyles(styles)(TableHistory);
