import React from 'react';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import PropTypes from 'prop-types';
import CircularProgress from '@material-ui/core/CircularProgress';
import Checkbox from '@material-ui/core/Checkbox';

const styles = {
  link: {
    cursor: 'pointer',
    textDecoration: 'none',
  },
  bold: { fontWeight: 900 },
  tableCell: {
    padding: '4px',
    textAlign: 'center',
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
    tableColumns: PropTypes.array.isRequired,
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
    if (qaTests && Array.isArray(qaTests)) {
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
    const { row } = this.props;
    const lastProcessed =
      this.props.lastProcessedId === row.pk ? styles.bold : null;
    return (
      <TableRow style={lastProcessed}>
        {this.props.tableColumns.map((column, key) => {
          const id = column.processKey.includes('exposure__')
            ? column.processKey.split('__')[1]
            : column.processKey;
          switch (column.type) {
            case 'parent':
              return (
                <TableCell key={`PROCV${key}`} style={styles.tableCell}>
                  {row[id]}
                </TableCell>
              );
            case 'normal':
              return (
                <TableCell key={`PROCV${key}`} style={styles.tableCell}>
                  {row.exposure[id]}
                </TableCell>
              );
            case 'date':
              return (
                <TableCell key={`PROCV${key}`} style={styles.tableCell}>
                  {this.formatDate(row.exposure[id])}
                </TableCell>
              );
            case 'dateprocess':
              return (
                <TableCell key={`PROCV${key}`} style={styles.tableCell}>
                  {this.formatDate(row[id])}
                </TableCell>
              );
            case 'time':
              return (
                <TableCell key={`PROCV${key}`} style={styles.tableCell}>
                  {this.formatTime(row.exposure.dateobs)}
                </TableCell>
              );
            case 'datemjd':
              return (
                <TableCell key={`PROCV${key}`} style={styles.tableCell}>
                  {row.datemjd.toFixed(2)}
                </TableCell>
              );
            case 'qa':
              return (
                <TableCell key={`PROCV${key}`} style={styles.tableCell}>
                  {this.renderViewQA(lastProcessed, row.runtime)}
                </TableCell>
              );
            default:
              return <TableCell key={`PROCV${key}`} style={styles.tableCell} />;
          }
        })}
      </TableRow>
    );
  };

  renderCheckbox = checked => {
    if (!this.props.selectable) return;
    return (
      <TableCell style={{ ...styles.tableCell }}>
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
      // selectedExposures,
      rowNumber,
      striped,
    } = this.props;
    const lastProcessed =
      lastProcessedId && lastProcessedId === processId ? styles.bold : null;
    // const selectedExposure =
    //   selectedExposures && selectedExposures.includes(rowNumber);

    return (
      <TableRow
        onClick={() => this.selectExposure(rowNumber)}
        style={lastProcessed}
        striped={striped}
      >
        {/* {this.renderCheckbox(selectedExposure)} */}
        {this.props.tableColumns
          .filter(column => column.exposureKey !== null)
          .map((column, key) => {
            const id = column.exposureKey;
            switch (column.type) {
              case 'parent':
              case 'normal':
                return (
                  <TableCell key={`EXPV${key}`} style={styles.tableCell}>
                    {row[id]}
                  </TableCell>
                );
              case 'date':
                return (
                  <TableCell key={`EXPV${key}`} style={styles.tableCell}>
                    {this.formatDate(row[id])}
                  </TableCell>
                );
              case 'dateprocess':
                return (
                  <TableCell key={`EXPV${key}`} style={styles.tableCell}>
                    {this.formatDate(row[id])}
                  </TableCell>
                );
              case 'time':
                return (
                  <TableCell key={`EXPV${key}`} style={styles.tableCell}>
                    {this.formatTime(row.dateobs)}
                  </TableCell>
                );
              case 'datemjd':
                return (
                  <TableCell key={`EXPV${key}`} style={styles.tableCell}>
                    {row.datemjd.toFixed(2)}
                  </TableCell>
                );
              case 'qa':
                return (
                  <TableCell key={`EXPV${key}`} style={styles.tableCell}>
                    {lastProcessedId &&
                    processId &&
                    lastProcessedId !== processId ? (
                      <span
                        style={styles.link}
                        onClick={() => selectProcessQA(processId)}
                      >
                        {this.qaSuccess()}
                      </span>
                    ) : null}
                  </TableCell>
                );
              default:
                return (
                  <TableCell key={`EXPV${key}`} style={styles.tableCell} />
                );
            }
          })}
      </TableRow>
    );
  };

  render() {
    return this.props.type === 'process'
      ? this.renderProcessingHistory()
      : this.renderObservingHistory();
  }
}
