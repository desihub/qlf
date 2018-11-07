import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import TableHistory from './widgets/table-history/table-history';
import SelectDate from '../../components/select-date/select-date';
import SelectNight from './widgets/select-night/select-night';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import Toolbar from '@material-ui/core/Toolbar';
import Icon from '@material-ui/core/Icon';
import Dialog from '@material-ui/core/Dialog';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogContent from '@material-ui/core/DialogContent';
import QlfApi from '../../containers/offline/connection/qlf-api';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import DialogActions from '@material-ui/core/DialogActions';

const styles = {
  card: {
    borderLeft: 'solid 4px #424242',
    flex: '1',
    height: 'calc(100vh - 2em - 66px)',
    margin: '1em',
    width: '95vw',
  },
  grid: {
    display: 'grid',
    gridTemplateRows: '6.5vh calc(100vh - 98px - 6.5vh)',
    height: 'calc(100vh - 98px)',
  },
  tableBody: {
    overflow: 'auto',
  },
  tableBodyHistory: {
    overflow: 'auto',
    height: 'calc(100vh - 98px - 6.5vh - 6.5vh)',
  },
  submit: {
    paddingLeft: '16px',
    cursor: ' pointer',
    fontSize: '1.2vw',
    verticalAlign: 'middle',
  },
  historyContainer: { WebkitAppRegion: 'no-drag' },
  tabItem: {
    fontSize: '1.2vw',
  },
  toolbar: {
    minHeight: '6.5vh',
    backgroundColor: 'rgb(232, 232, 232)',
    display: 'flex',
    justifyContent: 'space-between',
    paddingLeft: '1.25vw',
    paddingRight: '1.25vw',
  },
  tabsH: {
    minHeight: '6.5vh',
  },
  tabWH: {
    minWidth: '11vw',
    minHeight: '6.5vh',
  },
  ico: {
    paddingLeft: '1.25vw',
  },
  divisor: {
    backgroundColor: 'rgba(0, 0, 0, 0.176)',
    display: 'inline-block',
    width: '1px',
    color: 'rgba(0, 0, 0, 0.4)',
    lineHeight: '56px',
    height: '3.4vh',
    marginLeft: '1.25vw',
    verticalAlign: 'middle',
  },
  button: {
    fontSize: '1.1vw',
  },
  text: {
    fontSize: '1.2vw',
  },
  flexBox: {
    display: 'flex',
  },
  flexBoxInner: {
    display: 'flex',
    alignItems: 'center',
  },
  btnSubmit: {
    lineHeight: '6.5vh',
  },
};

class History extends Component {
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
    classes: PropTypes.object.isRequired,
  };

  constructor(props) {
    super(props);
    const renderTabs =
      process.env.REACT_APP_OFFLINE !== 'true' &&
      window.location.pathname !== '/survey-report';
    this.state = {
      renderTabs,
      tab: renderTabs ? 'last' : 'history',
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
          row={true}
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
    const { classes } = this.props;
    return (
      <Toolbar className={classes.toolbar}>
        <div className={classes.flexBox}>
          <div className={classes.flexBoxInner}>
            <Icon
              className="material-icons"
              title="Clear QA"
              onClick={() => this.props.navigateToQA(0)}
              style={styles.text}
            >
              clear_all
            </Icon>
            <span className={classes.divisor} />
            <Icon
              className="material-icons"
              title="Refresh"
              onClick={this.refreshRows}
              style={styles.text}
              classes={{ root: classes.ico }}
            >
              refresh
            </Icon>
            <span className={classes.divisor} />
          </div>
          {this.renderSelectDate()}
        </div>
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
    const { classes } = this.props;
    if (this.state.selectedExposures.length < 1) return;
    return (
      <div className={classes.btnSubmit}>
        <span className={classes.divisor} />
        <span
          className={classes.submit}
          title="Reprocess"
          onClick={this.handleOpenDialog}
        >
          Submit
        </span>
      </div>
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
    const { classes } = this.props;
    return (
      <div className={classes.tableBody}>
        {this.props.type === 'process'
          ? this.renderRecentProcesses()
          : this.renderRecentExposures()}
      </div>
    );
  };

  renderHistory = () => {
    const { classes } = this.props;
    return (
      <div>
        <div className={classes.tableBodyHistory}>{this.renderRows()}</div>
        {this.renderToolbar()}
      </div>
    );
  };

  handleTabChange = (evt, tab) => {
    this.setState({ tab });
  };

  renderTabs = () => {
    const { tab } = this.state;
    const { classes } = this.props;
    return (
      <div className={classes.grid}>
        <Tabs
          value={tab}
          onChange={this.handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
          className={classes.tabsH}
        >
          <Tab
            label="Most Recent"
            value={'last'}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="History"
            value={'history'}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
        </Tabs>
        {tab === 'last' ? this.renderLast() : null}
        {tab === 'history' ? this.renderHistory() : null}
      </div>
    );
  };

  render() {
    const { classes } = this.props;
    const actions = [
      <Button
        key={0}
        primary={true}
        onClick={this.handleCloseDialog}
        className={classes.button}
      >
        Cancel
      </Button>,
      <Button
        key={1}
        primary={true}
        onClick={this.reprocessExposure}
        className={classes.button}
      >
        Submit
      </Button>,
    ];

    return (
      <div className={classes.historyContainer}>
        <Dialog
          actions={actions}
          modal={false}
          open={this.state.confirmDialog}
          onRequestClose={this.handleClose}
        >
          <DialogContent>
            <DialogContentText classes={{ root: classes.text }}>
              Reprocess {this.exposuresToReprocess()}?
            </DialogContentText>
            <DialogActions>{actions}</DialogActions>
          </DialogContent>
        </Dialog>
        <Card className={classes.card}>
          {!this.state.renderTabs ? this.renderHistory() : this.renderTabs()}
        </Card>
      </div>
    );
  }
}

export default withStyles(styles)(History);
