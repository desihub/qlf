import React from 'react';
import { TableRow, TableRowColumn } from 'material-ui/Table';
import PropTypes from 'prop-types';
import Checkbox from 'material-ui/Checkbox';

const styles = {
  link: {
    cursor: 'pointer',
    textDecoration: 'none',
  },
  bold: { fontWeight: 900 },
  checkbox: {
    marginTop: '12px',
    marginLeft: '24px',
  },
};

export default class HistoryData extends React.Component {
  static muiName = 'TableRow';
  static propTypes = {
    processId: PropTypes.number,
    lastProcessedId: PropTypes.number,
    row: PropTypes.object,
    type: PropTypes.string,
    children: PropTypes.array,
    selectProcessQA: PropTypes.func.isRequired,
    selectedExposures: PropTypes.array,
    onCellClick: PropTypes.func,
    onCellHover: PropTypes.func,
    onCellHoverExit: PropTypes.func,
    onRowClick: PropTypes.func,
    onRowHover: PropTypes.func,
    onRowHoverExit: PropTypes.func,
    rowNumber: PropTypes.number,
    displayBorder: PropTypes.bool,
    striped: PropTypes.bool,
  };

  formatDate = dateString => {
    const date = new Date(dateString);
    const month = (date.getMonth() + 1 < 10 ? '0' : '') + (date.getMonth() + 1);
    const day = (date.getDate() + 1 < 10 ? '0' : '') + date.getDate();
    return month + '/' + day + '/' + date.getFullYear();
  };

  formatTime = dateString => {
    const time = new Date(dateString);
    const hour = (time.getHours() + 1 < 10 ? '0' : '') + time.getHours();
    const minutes = (time.getMinutes() + 1 < 10 ? '0' : '') + time.getMinutes();
    const seconds = (time.getSeconds() + 1 < 10 ? '0' : '') + time.getDate();
    return hour + ':' + minutes + ':' + seconds;
  };

  renderProcessingHistory = () => {
    const lastProcessed =
      this.props.lastProcessedId === this.props.row.pk ? styles.bold : null;
    return (
      <TableRow style={lastProcessed}>
        <TableRowColumn />
        <TableRowColumn>{this.props.row.pk}</TableRowColumn>
        <TableRowColumn>{this.formatDate(this.props.row.start)}</TableRowColumn>
        <TableRowColumn>{this.props.row.runtime}</TableRowColumn>
        <TableRowColumn>{this.props.row.exposure_id}</TableRowColumn>
        <TableRowColumn>{this.props.row.tile}</TableRowColumn>
        <TableRowColumn>
          {this.formatDate(this.props.row.dateobs)}
        </TableRowColumn>
        <TableRowColumn>
          {this.formatTime(this.props.row.dateobs)}
        </TableRowColumn>
        <TableRowColumn>{this.props.row.datemjd.toFixed(2)}</TableRowColumn>
        <TableRowColumn>{this.props.row.telra}</TableRowColumn>
        <TableRowColumn>{this.props.row.teldec}</TableRowColumn>
        <TableRowColumn>{this.props.row.exptime}</TableRowColumn>
        <TableRowColumn>{this.props.row.airmass}</TableRowColumn>
        <TableRowColumn />
        <TableRowColumn>
          <span
            style={styles.link}
            onClick={() => this.props.selectProcessQA(this.props.processId)}
          >
            View
          </span>
        </TableRowColumn>
        <TableRowColumn />
      </TableRow>
    );
  };

  renderObservingHistory = () => {
    const {
      processId,
      selectProcessQA,
      row,
      lastProcessedId,
      selectedExposures,
      children,
      onCellClick,
      onCellHover,
      onCellHoverExit,
      onRowClick,
      onRowHover,
      onRowHoverExit,
      rowNumber,
      displayBorder,
      striped,
    } = this.props;
    const lastProcessed = lastProcessedId === processId ? styles.bold : null;
    const selectedExposure =
      selectedExposures && selectedExposures.includes(rowNumber);
    return (
      <TableRow
        style={lastProcessed}
        onCellClick={onCellClick}
        onCellHover={onCellHover}
        onCellHoverExit={onCellHoverExit}
        onRowClick={onRowClick}
        onRowHover={onRowHover}
        onRowHoverExit={onRowHoverExit}
        rowNumber={rowNumber}
        displayBorder={displayBorder}
        striped={striped}
      >
        {children[0] ? (
          <Checkbox checked={selectedExposure} style={styles.checkbox} />
        ) : (
          children[0]
        )}
        <TableRowColumn />
        <TableRowColumn>{row.exposure_id}</TableRowColumn>
        <TableRowColumn>{row.tile}</TableRowColumn>
        <TableRowColumn>{this.formatDate(row.dateobs)}</TableRowColumn>
        <TableRowColumn>{this.formatTime(row.dateobs)}</TableRowColumn>
        <TableRowColumn>{row.datemjd.toFixed(2)}</TableRowColumn>
        <TableRowColumn>{row.telra}</TableRowColumn>
        <TableRowColumn>{row.teldec}</TableRowColumn>
        <TableRowColumn>{row.exptime}</TableRowColumn>
        <TableRowColumn>{row.airmass}</TableRowColumn>
        <TableRowColumn />
        <TableRowColumn>
          <span style={styles.link} onClick={() => selectProcessQA(processId)}>
            View
          </span>
        </TableRowColumn>
        <TableRowColumn />
      </TableRow>
    );
  };

  render() {
    return this.props.type === 'process'
      ? this.renderProcessingHistory()
      : this.renderObservingHistory();
  }
}
