import React, { Component } from 'react';
import PropTypes from 'prop-types';
import HistoryHeader from './history-header/history-header';
import HistoryData from './history-data/history-data';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TablePagination from '@material-ui/core/TablePagination';
import { processColumns } from './process-columns';
import { exposureColumns } from './exposure-columns';
import Modal from '@material-ui/core/Modal';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';
import CommentModal from '../comment-modal/comment-modal';

class TableHistory extends Component {
  static propTypes = {
    getHistory: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    selectExposure: PropTypes.func,
    type: PropTypes.string.isRequired,
    selectable: PropTypes.bool,
    orderable: PropTypes.bool,
    processId: PropTypes.string,
    lastProcessedId: PropTypes.string,
    selectedExposures: PropTypes.array,
    rowsCount: PropTypes.number,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    classes: PropTypes.object.isRequired,
    changeLimit: PropTypes.func.isRequired,
    limit: PropTypes.number.isRequired,
    fetchLastProcess: PropTypes.func.isRequired,
    pipelineRunning: PropTypes.string,
    openCCDViewer: PropTypes.func.isRequired,
    openLogViewer: PropTypes.func,
    handleHistoryStateChange: PropTypes.func,
    night: PropTypes.string,
  };

  constructor(props) {
    super(props);
    this.state = {
      asc: false,
      ordering: this.props.type === 'process' ? 'exposure__dateobs' : 'dateobs',
      order: this.props.type === 'process' ? '-exposure__dateobs' : '-dateobs',
      offset: 0,
      filters: '',
      flavorFilter: '',
      statusFilter: '',
      tableColumnsHidden: [],
      openColumnsModal: false,
      openCommentModal: false,
      commentProcessId: 1,
    };
  }

  componentDidMount() {
    if (this.props.handleHistoryStateChange) {
      this.props.handleHistoryStateChange('order', this.state.order);
      this.props.handleHistoryStateChange('offset', this.state.offset);
      this.props.handleHistoryStateChange('filters', this.state.filters);
    }
  }

  componentWillReceiveProps(nextProps) {
    if (
      nextProps.startDate &&
      nextProps.endDate &&
      (this.props.startDate !== nextProps.startDate ||
        this.props.endDate !== nextProps.endDate)
    ) {
      const { asc, ordering } = this.state;
      const order = asc ? ordering : `-${ordering}`;
      this.props.getHistory(
        nextProps.startDate,
        nextProps.endDate,
        order,
        this.state.offset,
        this.props.limit,
        this.state.filters,
        this.props.night
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
              processId={String(processId)}
              row={row}
              rowNumber={id}
              selectProcessQA={this.selectProcessQA}
              type={this.props.type}
              lastProcessedId={this.props.lastProcessedId}
              selectedExposures={this.props.selectedExposures}
              selectExposure={this.props.selectExposure}
              selectable={this.props.selectable}
              tableColumns={this.availableColumns()}
              openCCDViewer={this.openCCDViewer}
              handleCommentModalOpen={this.handleCommentModalOpen}
              pipelineRunning={this.props.pipelineRunning}
              openLogViewer={this.props.openLogViewer}
            />
          );
        })}
      </TableBody>
    );
  };

  addOrder = (ordering, asc) => {
    const order = asc ? ordering : `-${ordering}`;
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      order,
      this.state.offset,
      this.props.limit,
      this.state.filters,
      this.props.night
    );
    this.setState({
      asc,
      ordering,
      order,
      offset: 0,
    });
    this.props.handleHistoryStateChange('order', order);
  };

  addStatusFilter = filter => {
    let statusFilter = '';
    switch (filter) {
      case 'all':
        break;
      case 'fail':
        statusFilter = 'status=1';
        break;
      case 'normal':
        statusFilter = 'status=0&end__isnull=False';
        break;
      case 'abort':
        statusFilter = 'end__isnull=True';
        break;
      default:
        break;
    }
    const filters = `${this.state.flavorFilter}&${statusFilter}`;
    this.setState({ statusFilter, filters });
    this.props.handleHistoryStateChange('filters', filters);
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      this.state.order,
      this.state.offset,
      this.props.limit,
      filters,
      this.props.night
    );
  };

  addFlavorFilter = flavorFilter => {
    const filters = `${flavorFilter}&${this.state.statusFilter}`;
    this.setState({ flavorFilter, filters });
    this.props.handleHistoryStateChange('filters', filters);
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      this.state.order,
      this.state.offset,
      this.props.limit,
      filters,
      this.props.night
    );
  };

  handleChangePage = (evt, offset) => {
    this.props.handleHistoryStateChange('offset', offset);
    this.props.getHistory(
      this.props.startDate,
      this.props.endDate,
      this.state.order,
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
      this.state.order,
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

  renderColumnsModal = () => {
    const availableColumns =
      this.props.type === 'process' ? processColumns : exposureColumns;
    return (
      <Modal
        open={this.state.openColumnsModal}
        onClose={this.handleColumnModalClose}
        className={this.props.classes.modal}
      >
        <div className={this.props.classes.modalBody}>
          <FormControl component="fieldset">
            <FormLabel component="legend">Avaiable Columns</FormLabel>
            <FormGroup className={this.props.classes.columnsFormGroup}>
              {availableColumns.map(column => (
                <FormControlLabel
                  key={`CHECK${column.name}`}
                  control={
                    <Checkbox
                      checked={Boolean(
                        !this.state.tableColumnsHidden.find(
                          c => c === column.name
                        )
                      )}
                      onChange={() => this.handleChangeColumns(column.name)}
                    />
                  }
                  label={column.name}
                />
              ))}
            </FormGroup>
          </FormControl>
          <div>
            <Button
              className={this.props.classes.modalColumnsButtonClose}
              onClick={this.handleColumnModalClose}
            >
              Close
            </Button>
            <Button
              className={this.props.classes.modalColumnsButtonClose}
              onClick={this.hadleSelectNone}
            >
              None
            </Button>
            <Button
              className={this.props.classes.modalColumnsButtonClose}
              onClick={this.handleSelectall}
            >
              All
            </Button>
          </div>
        </div>
      </Modal>
    );
  };

  handleSelectall = () => {
    this.setState({ tableColumnsHidden: [] });
  };

  hadleSelectNone = () => {
    const availableColumns =
      this.props.type === 'process'
        ? processColumns.map(c => c.name)
        : exposureColumns.map(c => c.name);
    this.setState({ tableColumnsHidden: availableColumns });
  };

  handleChangeColumns = name => {
    const { tableColumnsHidden } = this.state;
    if (!tableColumnsHidden.find(c => c === name)) {
      this.setState({
        tableColumnsHidden: tableColumnsHidden.concat(name),
      });
    } else {
      this.setState({
        tableColumnsHidden: tableColumnsHidden.filter(tch => tch !== name),
      });
    }
  };

  availableColumns = () => {
    const availableColumns =
      this.props.type === 'process' ? processColumns : exposureColumns;
    return availableColumns.filter(
      tc => !this.state.tableColumnsHidden.includes(tc.name)
    );
  };

  openColumnsModal = () => {
    this.setState({
      openColumnsModal: true,
    });
  };

  handleColumnModalClose = () => {
    this.setState({
      openColumnsModal: false,
    });
  };

  openCCDViewer = (night, exposureId) => {
    this.props.openCCDViewer(night, exposureId);
  };

  renderCommentModal = () => {
    return this.state.openCommentModal ? (
      <CommentModal
        processId={this.state.commentProcessId}
        handleClose={this.handleCommentModalClose}
        readOnly={this.props.type !== 'process'}
        fetchLastProcess={this.props.fetchLastProcess}
      />
    ) : null;
  };

  handleCommentModalOpen = commentProcessId => {
    this.setState({
      commentProcessId,
      openCommentModal: true,
    });
  };

  handleCommentModalClose = () => {
    this.setState({
      openCommentModal: false,
    });
  };

  render() {
    return (
      <div className={this.props.classes.root}>
        {this.renderCommentModal()}
        {this.renderColumnsModal()}
        <Table style={styles.table}>
          <HistoryHeader
            addOrder={this.addOrder}
            addFlavorFilter={this.addFlavorFilter}
            addStatusFilter={this.addStatusFilter}
            type={this.props.type}
            asc={this.state.asc}
            ordering={this.state.ordering}
            selectable={this.props.selectable}
            orderable={this.props.orderable}
            selectExposure={this.props.selectExposure}
            tableColumns={this.availableColumns()}
            openColumnsModal={this.openColumnsModal}
          />
          {this.renderBody()}
        </Table>
        {this.props.night ? null : this.renderPagination()}
      </div>
    );
  }
}

const styles = {
  root: {
    width: '100%',
  },
  table: {
    textAlign: 'center',
    width: '100%',
    tableLayout: 'auto',
    overflowX: 'auto',
  },
  modalBody: {
    position: 'absolute',
    backgroundColor: 'white',
    boxShadow: 1,
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
  },
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  columnsFormGroup: {
    display: 'grid',
    gridTemplateColumns: 'auto auto auto auto auto',
  },
  modalColumnsButtonClose: {
    float: 'right',
  },
};

export default withStyles(styles)(TableHistory);
