import React from 'react';
import { TableRow, TableCell } from 'material-ui-next/Table';
import PropTypes from 'prop-types';
import Checkbox from 'material-ui/Checkbox';
import { CircularProgress } from 'material-ui-next/Progress';

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
    selectable: PropTypes.bool,
    selectExposure: PropTypes.func,
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

  renderViewQA = (lastProcessed, runtime) => {
    if (lastProcessed && !runtime) return <CircularProgress size={20} />;
    if (!runtime) return;
    return (
      <span
        style={styles.link}
        onClick={() => this.props.selectProcessQA(this.props.processId)}
      >
        View
      </span>
    );
  };

  renderProcessingHistory = () => {
    const lastProcessed =
      this.props.lastProcessedId === this.props.row.pk ? styles.bold : null;
    return (
      <TableRow style={lastProcessed}>
        <TableCell />
        <TableCell>{this.props.row.pk}</TableCell>
        <TableCell>{this.formatDate(this.props.row.start)}</TableCell>
        <TableCell>{this.props.row.runtime}</TableCell>
        <TableCell>{this.props.row.exposure.exposure_id}</TableCell>
        <TableCell>{this.props.row.exposure.tile}</TableCell>
        <TableCell>
          {this.formatDate(this.props.row.exposure.dateobs)}
        </TableCell>
        <TableCell>
          {this.formatTime(this.props.row.exposure.dateobs)}
        </TableCell>
        <TableCell>{this.props.row.datemjd.toFixed(2)}</TableCell>
        <TableCell>{this.props.row.exposure.telra}</TableCell>
        <TableCell>{this.props.row.exposure.teldec}</TableCell>
        <TableCell>{this.props.row.exposure.exptime}</TableCell>
        <TableCell>{this.props.row.exposure.flavor}</TableCell>
        <TableCell>{this.props.row.exposure.airmass}</TableCell>
        <TableCell />
        <TableCell>
          {this.renderViewQA(lastProcessed, this.props.row.runtime)}
        </TableCell>
        <TableCell />
      </TableRow>
    );
  };

  renderCheckbox = checked => {
    if (!this.props.selectable) return;
    return (
      <TableCell padding="checkbox">
        <Checkbox checked={checked} />
      </TableCell>
    );
  };

  selectExposure = rowNumber => {
    if (this.props.selectExposure) this.props.selectExposure([rowNumber]);
  };

  renderObservingHistory = () => {
    const {
      processId,
      selectProcessQA,
      row,
      lastProcessedId,
      selectedExposures,
      rowNumber,
      striped,
    } = this.props;
    const lastProcessed = lastProcessedId === processId ? styles.bold : null;
    const selectedExposure =
      selectedExposures && selectedExposures.includes(rowNumber);
    const {
      exposure_id,
      tile,
      dateobs,
      telra,
      teldec,
      exptime,
      flavor,
      airmass,
    } = row;
    return (
      <TableRow
        onClick={() => this.selectExposure(rowNumber)}
        style={lastProcessed}
        striped={striped}
      >
        {this.renderCheckbox(selectedExposure)}
        <TableCell />
        <TableCell>{exposure_id}</TableCell>
        <TableCell>{tile}</TableCell>
        <TableCell>{this.formatDate(dateobs)}</TableCell>
        <TableCell>{this.formatTime(dateobs)}</TableCell>
        <TableCell>{row.datemjd.toFixed(2)}</TableCell>
        <TableCell>{telra}</TableCell>
        <TableCell>{teldec}</TableCell>
        <TableCell>{exptime}</TableCell>
        <TableCell>{flavor}</TableCell>
        <TableCell>{airmass}</TableCell>
        <TableCell />
        <TableCell>
          <span style={styles.link} onClick={() => selectProcessQA(processId)}>
            View
          </span>
        </TableCell>
        <TableCell />
      </TableRow>
    );
  };

  render() {
    return this.props.type === 'process'
      ? this.renderProcessingHistory()
      : this.renderObservingHistory();
  }
}
