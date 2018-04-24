import React from 'react';
import { TableRow, TableRowColumn } from 'material-ui/Table';
import PropTypes from 'prop-types';

const styles = {
  link: {
    cursor: 'pointer',
    textDecoration: 'none',
  },
  bold: { fontWeight: 900 },
};

export default class HistoryData extends React.Component {
  static muiName = 'TableRow';
  static propTypes = {
    lastProcess: PropTypes.number,
    processId: PropTypes.number,
    row: PropTypes.object,
    type: PropTypes.string,
    children: PropTypes.array,
    selectProcessQA: PropTypes.func.isRequired,
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
    const lastProcessStyle =
      process.pk === this.props.lastProcess ? styles.bold : null;
    return (
      <TableRow style={lastProcessStyle}>
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
      lastProcess,
      selectProcessQA,
      row,
      ...otherProps
    } = this.props;
    const lastProcessStyle =
      this.props.row.pk === lastProcess ? styles.bold : null;
    return (
      <TableRow style={lastProcessStyle} {...otherProps}>
        {this.props.children[0]}
        <TableRowColumn />
        <TableRowColumn>{row.pk}</TableRowColumn>
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
