import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableHistory from './widgets/table-history/table-history';
import SelectDate from './widgets/select-date/select-date';
import { Tabs, Tab } from 'material-ui/Tabs';
import { Card } from 'material-ui/Card';
import { Toolbar, ToolbarGroup, ToolbarSeparator } from 'material-ui/Toolbar';
import FontIcon from 'material-ui/FontIcon';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import QlfApi from '../../containers/offline/connection/qlf-api';
import _ from 'lodash';

const styles = {
  card: {
    borderLeft: 'solid 4px teal',
    flex: '1',
    height: '90%',
    margin: '1em',
  },
};

export default class History extends Component {
  static propTypes = {
    getHistory: PropTypes.func.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    lastProcesses: PropTypes.array,
    type: PropTypes.string.isRequired,
    lastProcessedId: PropTypes.number,
    rowsCount: PropTypes.number,
  };

  renderSelectDate = () => {
    if (this.props.startDate && this.props.endDate)
      return (
        <SelectDate
          startDate={this.props.startDate}
          endDate={this.props.endDate}
          setHistoryRangeDate={this.setHistoryRangeDate}
        />
      );
  };

  setHistoryRangeDate = (startDate, endDate) => {
    this.setState({ startDate, endDate });
  };

  state = {
    tab: 'history',
    confirmDialog: false,
    selectedExposures: [],
    startDate: this.props.startDate,
    endDate: this.props.endDate,
    limit: 10,
  };

  changeLimit = limit => {
    this.setState({ limit });
  };

  componentWillReceiveProps(nextProps) {
    if (nextProps.startDate && nextProps.endDate) {
      this.setState({
        startDate: nextProps.startDate,
        endDate: nextProps.endDate,
      });
    }
  }

  renderLastProcesses = () => {
    let lastProcesses = this.props.lastProcesses
      ? this.props.lastProcesses
      : [];
    if (this.props.type === 'exposure')
      lastProcesses = _.uniq(lastProcesses.map(lp => lp.exposure_id)).map(exp =>
        _.maxBy(lastProcesses.filter(lp => lp.exposure_id === exp), 'pk')
      );
    return (
      <TableHistory
        getHistory={this.props.getHistory}
        rows={lastProcesses}
        navigateToQA={this.props.navigateToQA}
        type={this.props.type}
        selectable={false}
        orderable={false}
        startDate={this.state.startDate}
        endDate={this.state.endDate}
        lastProcessedId={this.props.lastProcessedId}
        changeLimit={this.changeLimit}
        limit={this.state.limit}
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
          selectable={true}
          orderable={true}
          lastProcessedId={this.props.lastProcessedId}
          selectExposure={this.selectExposure}
          selectedExposures={this.state.selectedExposures}
          rowsCount={this.props.rowsCount}
          changeLimit={this.changeLimit}
          limit={this.state.limit}
        />
      );
    }
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
            onClick={() =>
              this.props.getHistory(
                this.props.startDate,
                this.props.endDate,
                '-pk',
                0,
                this.state.limit
              )
            }
          >
            refresh
          </FontIcon>
          <ToolbarSeparator />
          {this.renderSelectDate()}
        </ToolbarGroup>
        {this.renderReprocessButton()}
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
        <FontIcon
          className="material-icons"
          title="Reprocess"
          onClick={this.handleOpenDialog}
        >
          play_arrow
        </FontIcon>
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
      <div style={{ WebkitAppRegion: 'no-drag' }}>
        <Dialog
          actions={actions}
          modal={false}
          open={this.state.confirmDialog}
          onRequestClose={this.handleClose}
        >
          Reprocess {this.exposuresToReprocess()}?
        </Dialog>
        <Card style={styles.card}>
          <Tabs value={this.state.value} onChange={this.handleChange}>
            <Tab label="Most Recent" value="last">
              {this.renderLastProcesses()}
            </Tab>
            <Tab label="History" value="history">
              {this.renderToolbar()}
              {this.renderRows()}
            </Tab>
          </Tabs>
        </Card>
      </div>
    );
  }
}
