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
  tableCheckbox: {
    paddingLeft: '23px',
  },
  tableCell: {
    padding: '4px 4px 4px 4px',
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

  qaSuccess = () => {
    const { row } = this.props;
    const qaTests = row.qa_tests
      ? row.qa_tests
      : row.last_exposure_process_qa_tests
        ? row.last_exposure_process_qa_tests
        : null;
    if (qaTests) {
      const testsFailed =
        !JSON.stringify(qaTests).includes('None') &&
        !JSON.stringify(qaTests).includes('FAILURE');
      return this.renderQAStatus(testsFailed);
    }
    return this.renderQAStatus(false);
  };

  renderQAStatus = status => {
    return status ? (
      <span style={{ color: 'green' }}>✓</span>
    ) : (
      <span style={{ color: 'red' }}>✖︎</span>
    );
  };

  renderViewQA = (lastProcessed, runtime) => {
    if (lastProcessed && !runtime) return <CircularProgress size={20} />;
    if (!runtime) return;

    return (
      <span
        style={styles.link}
        onClick={() => this.props.selectProcessQA(this.props.processId)}
      >
        {this.qaSuccess()}
      </span>
    );
  };

  renderProcessingHistory = () => {
    const lastProcessed =
      this.props.lastProcessedId === this.props.row.pk ? styles.bold : null;
    return (
      <TableRow style={lastProcessed}>
        <TableCell style={styles.tableCell} />
        <TableCell style={styles.tableCell}>{this.props.row.pk}</TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.exposure.exposure_id}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.exposure.tile}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.formatDate(this.props.row.start)}
        </TableCell>
        <TableCell style={styles.tableCell}>{this.props.row.runtime}</TableCell>
        <TableCell style={styles.tableCell}>
          {this.formatDate(this.props.row.exposure.dateobs)}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.formatTime(this.props.row.exposure.dateobs)}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.datemjd.toFixed(2)}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.exposure.telra}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.exposure.teldec}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.exposure.exptime}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.exposure.flavor}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.props.row.exposure.airmass}
        </TableCell>
        <TableCell style={styles.tableCell} />
        <TableCell style={styles.tableCell}>
          {this.renderViewQA(lastProcessed, this.props.row.runtime)}
        </TableCell>
        <TableCell style={styles.tableCell} />
      </TableRow>
    );
  };

  renderCheckbox = checked => {
    if (!this.props.selectable) return;
    return (
      <TableCell
        style={{ ...styles.tableCell, ...styles.tableCheckbox }}
        padding="checkbox"
      >
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
        <TableCell style={styles.tableCell} />
        <TableCell style={styles.tableCell}>{exposure_id}</TableCell>
        <TableCell style={styles.tableCell}>{tile}</TableCell>
        <TableCell style={styles.tableCell}>
          {this.formatDate(dateobs)}
        </TableCell>
        <TableCell style={styles.tableCell}>
          {this.formatTime(dateobs)}
        </TableCell>
        <TableCell style={styles.tableCell}>{row.datemjd.toFixed(2)}</TableCell>
        <TableCell style={styles.tableCell}>{telra}</TableCell>
        <TableCell style={styles.tableCell}>{teldec}</TableCell>
        <TableCell style={styles.tableCell}>{exptime}</TableCell>
        <TableCell style={styles.tableCell}>{flavor}</TableCell>
        <TableCell style={styles.tableCell}>{airmass}</TableCell>
        <TableCell style={styles.tableCell} />
        <TableCell style={styles.tableCell}>
          {processId && lastProcessedId !== processId ? (
            <span
              style={styles.link}
              onClick={() => selectProcessQA(processId)}
            >
              {this.qaSuccess()}
            </span>
          ) : null}
        </TableCell>
        <TableCell style={styles.tableCell} />
      </TableRow>
    );
  };

  render() {
    return this.props.type === 'process'
      ? this.renderProcessingHistory()
      : this.renderObservingHistory();
  }
}
