import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableHistory from './widgets/table-history/table-history';
import SelectDate from './widgets/select-date/select-date';
import SelectNight from './widgets/select-night/select-night';
import { Card } from 'material-ui/Card';
import { Toolbar, ToolbarGroup, ToolbarSeparator } from 'material-ui/Toolbar';
import FontIcon from 'material-ui/FontIcon';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import QlfApi from '../../containers/offline/connection/qlf-api';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

const styles = {
  card: {
    borderLeft: 'solid 4px #424242',
    flex: '1',
    height: '90%',
    margin: '1em',
    width: '95vw',
  },
  tableBody: {
    overflow: 'auto',
    height: 'calc(100vh - 160px)',
  },
  tableBodyHistory: {
    overflow: 'auto',
    height: 'calc(100vh - 216px)',
  },
  submit: {
    paddingLeft: '16px',
    cursor: ' pointer',
  },
  historyContainer: { WebkitAppRegion: 'no-drag' },
};

export default class History extends Component {
  static propTypes = {
    getHistory: PropTypes.func.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    recentProcesses: PropTypes.array,
    recentExposures: PropTypes.array,
    type: PropTypes.string.isRequired,
    lastProcessedId: PropTypes.string,
    rowsCount: PropTypes.number,
    fetchLastProcess: PropTypes.func.isRequired,
    pipelineRunning: PropTypes.string.isRequired,
    openCCDViewer: PropTypes.func.isRequired,
    openLogViewer: PropTypes.func,
  };

  constructor(props) {
    super(props);
    const renderTabs =
      process.env.REACT_APP_OFFLINE !== 'true' &&
      window.location.pathname !== '/survey-report';
    this.state = {
      renderTabs,
      tab: renderTabs ? 'history' : 'last',
      confirmDialog: false,
      selectedExposures: [],
      startDate: this.props.startDate,
      endDate: this.props.endDate,
      limit: 10,
      firstLoad: false,
      nights: undefined,
      night: undefined,
    };
  }

  componentDidMount() {
    switch (window.location.pathname) {
      case '/processing-history':
        document.title = 'Processing History';
        break;
      case '/observing-history':
        document.title = 'Observing History';
        break;
      case '/survey-report':
        document.title = 'Survey Reports';
        break;
      default:
        document.title = 'History';
    }
  }

  selectNight = dir => {
    const index = this.state.nights.indexOf(this.state.night);
    if (dir === 'next' && index < this.state.nights.length - 1) {
      this.setState({ night: this.state.nights[index + 1] }, this.refreshRows);
    } else if (dir !== 'next' && index > 0) {
      this.setState({ night: this.state.nights[index - 1] }, this.refreshRows);
    }
  };

  renderSelectDate = () => {
    if (window.location.pathname === '/survey-report') {
      return (
        <SelectNight night={this.state.night} selectNight={this.selectNight} />
      );
    } else if (this.props.startDate && this.props.endDate)
      return (
        <SelectDate
          startDate={this.props.startDate}
          endDate={this.props.endDate}
          setHistoryRangeDate={this.setHistoryRangeDate}
        />
      );
  };

  setHistoryRangeDate = (startDate, endDate) => {
    this.setState({
      startDate,
      endDate,
    });
  };

  changeLimit = limit => {
    this.setState({ limit });
  };

  componentWillMount() {
    if (window.location.pathname === '/survey-report') {
      this.storeAvailableNights();
    }
  }

  storeAvailableNights = async () => {
    const nightsApi = await QlfApi.getNights();
    if (nightsApi && nightsApi.results) {
      const nights = nightsApi.results.map(n => n.night);
      this.setState({ nights, night: nights[nights.length - 1] });
      this.refreshRows();
    }
  };

  componentWillReceiveProps(nextProps) {
    if (nextProps.startDate && nextProps.endDate) {
      if (!this.state.firstLoad) {
        this.props.fetchLastProcess();
        this.setState({
          startDate: nextProps.startDate,
          endDate: nextProps.endDate,
          firstLoad: true,
        });
      }
    }
  }

  renderRecentProcesses = () => {
    const recentProcesses = this.props.recentProcesses
      ? this.props.recentProcesses
      : [];
    return (
      <TableHistory
        getHistory={this.props.getHistory}
        rows={recentProcesses}
        navigateToQA={this.props.navigateToQA}
        type={this.props.type}
        selectable={false}
        orderable={false}
        startDate={this.state.startDate}
        endDate={this.state.endDate}
        lastProcessedId={this.props.lastProcessedId}
        changeLimit={this.changeLimit}
        limit={this.state.limit}
        fetchLastProcess={this.props.fetchLastProcess}
        pipelineRunning={this.props.pipelineRunning}
        openCCDViewer={this.props.openCCDViewer}
        openLogViewer={this.props.openLogViewer}
      />
    );
  };

  renderRecentExposures = () => {
    const recentExposures = this.props.recentExposures
      ? this.props.recentExposures
      : [];

    return (
      <TableHistory
        getHistory={this.props.getHistory}
        rows={recentExposures}
        navigateToQA={this.props.navigateToQA}
        type={this.props.type}
        selectable={false}
        orderable={false}
        startDate={this.state.startDate}
        endDate={this.state.endDate}
        lastProcessedId={this.props.lastProcessedId}
        changeLimit={this.changeLimit}
        limit={this.state.limit}
        fetchLastProcess={this.props.fetchLastProcess}
        openCCDViewer={this.props.openCCDViewer}
      />
    );
  };

  selectExposure = rows => {
    if (rows === true) {
      const selectedExposures = this.props.rows.map((row, id) => id);
      this.setState({ selectedExposures });
      return;
    }

    if (rows === false) {
      this.setState({ selectedExposures: [] });
      return;
    }

    const selectedExposures = this.state.selectedExposures.includes(rows[0])
      ? this.state.selectedExposures.filter(row => !rows.includes(row))
      : this.state.selectedExposures.concat(rows);
    this.setState({ selectedExposures });
  };

  handleHistoryStateChange = (key, value) => {
    this.setState({
      [key]: value,
    });
  };

  renderRows = () => {
    if (this.props.rows) {
      return (
        <TableHistory
          getHistory={this.props.getHistory}
          startDate={this.state.startDate}
          endDate={this.state.endDate}
          rows={this.props.rows}
          navigateToQA={this.props.navigateToQA}
          type={this.props.type}
          selectable={true && this.state.renderTabs}
          orderable={true}
          lastProcessedId={this.props.lastProcessedId}
          selectExposure={this.selectExposure}
          selectedExposures={this.state.selectedExposures}
          rowsCount={this.props.rowsCount}
          changeLimit={this.changeLimit}
          limit={this.state.limit}
          fetchLastProcess={this.props.fetchLastProcess}
          openCCDViewer={this.props.openCCDViewer}
          openLogViewer={this.props.openLogViewer}
          handleHistoryStateChange={this.handleHistoryStateChange}
          night={this.state.night}
        />
      );
    }
  };

  refreshRows = () => {
    this.props.getHistory(
      this.state.startDate,
      this.state.endDate,
      this.state.order,
      this.state.offset,
      this.state.limit,
      this.state.filters,
      this.state.night
    );
  };

  renderToolbar = () => {
    return (
      <Toolbar>
        <ToolbarGroup firstChild={true}>
          <FontIcon
            className="material-icons"
            title="Clear QA"
            onClick={() => this.props.navigateToQA(0)}
          >
            clear_all
          </FontIcon>
          <ToolbarSeparator />
          <FontIcon
            className="material-icons"
            title="Refresh"
            onClick={this.refreshRows}
          >
            refresh
          </FontIcon>
          <ToolbarSeparator />
          {this.renderSelectDate()}
        </ToolbarGroup>
        {!this.state.renderTabs ? null : this.renderReprocessButton()}
      </Toolbar>
    );
  };

  reprocessExposure = () => {
    const exposures = this.state.selectedExposures.map(
      exposure => this.props.rows[exposure].exposure_id
    );
    exposures.forEach(async exp => {
      await QlfApi.reprocessExposure(exp);
    });
    this.setState({ confirmDialog: false });
  };

  renderReprocessButton = () => {
    if (this.state.selectedExposures.length < 1) return;
    return (
      <ToolbarGroup>
        <ToolbarSeparator />
        <span
          style={styles.submit}
          title="Reprocess"
          onClick={this.handleOpenDialog}
        >
          Submit
        </span>
      </ToolbarGroup>
    );
  };

  handleOpenDialog = () => {
    this.setState({ confirmDialog: true });
  };

  handleCloseDialog = () => {
    this.setState({ confirmDialog: false });
  };

  exposuresToReprocess = () => {
    const exposures = this.state.selectedExposures
      .map(row => this.props.rows[row].exposure_id)
      .join(', ');
    return `exposure${exposures.length > 1 ? 's' : ''} ${exposures}`;
  };

  renderLast = () => {
    return (
      <div style={styles.tableBody}>
        {this.props.type === 'process'
          ? this.renderRecentProcesses()
          : this.renderRecentExposures()}
      </div>
    );
  };

  renderHistory = () => {
    return (
      <div>
        <div style={styles.tableBodyHistory}>{this.renderRows()}</div>
        {this.renderToolbar()}
      </div>
    );
  };

  handleTabChange = (evt, tab) => {
    this.setState({ tab });
  };

  renderTabs = () => {
    const { tab } = this.state;
    return (
      <div>
        <Tabs
          value={tab}
          onChange={this.handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
        >
          <Tab label="Most Recent" value={'last'} />
          <Tab label="History" value={'history'} />
        </Tabs>
        {tab === 'last' ? this.renderLast() : null}
        {tab === 'history' ? this.renderHistory() : null}
      </div>
    );
  };

  render() {
    const actions = [
      <FlatButton
        key={0}
        label="Cancel"
        primary={true}
        onClick={this.handleCloseDialog}
      />,
      <FlatButton
        key={1}
        label="Submit"
        primary={true}
        onClick={this.reprocessExposure}
      />,
    ];

    return (
      <div style={styles.historyContainer}>
        <Dialog
          actions={actions}
          modal={false}
          open={this.state.confirmDialog}
          onRequestClose={this.handleClose}
        >
          Reprocess {this.exposuresToReprocess()}?
        </Dialog>
        <Card style={styles.card}>
          {!this.state.renderTabs ? this.renderHistory() : this.renderTabs()}
        </Card>
      </div>
    );
  }
}
