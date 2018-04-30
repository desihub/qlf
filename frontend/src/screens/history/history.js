import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableHistory from './widgets/table-history/table-history';
import SelectDate from './widgets/select-date/select-date';
import { Tabs, Tab } from 'material-ui/Tabs';
import { Card } from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
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
    getHistoryOrdered: PropTypes.func.isRequired,
    navigateToQA: PropTypes.func.isRequired,
    rows: PropTypes.array.isRequired,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    getHistoryRangeDate: PropTypes.func.isRequired,
    lastProcesses: PropTypes.array,
    type: PropTypes.string.isRequired,
    lastProcessedId: PropTypes.number,
  };

  renderSelectDate = () => {
    if (this.props.startDate && this.props.endDate)
      return (
        <SelectDate
          startDate={this.props.startDate}
          endDate={this.props.endDate}
          getHistoryRangeDate={this.props.getHistoryRangeDate}
        />
      );
  };

  state = {
    tab: 'history',
  };

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
        getHistoryOrdered={this.props.getHistoryOrdered}
        rows={lastProcesses}
        navigateToQA={this.props.navigateToQA}
        type={this.props.type}
        selectable={false}
        orderable={false}
        lastProcessedId={this.props.lastProcessedId}
      />
    );
  };

  renderSubmit = () => {
    if (this.props.type === 'process') return;
    return (
      <RaisedButton
        label="Submit"
        backgroundColor={'#00C853'}
        labelStyle={{ color: 'white' }}
        fullWidth={true}
      />
    );
  };

  renderRows = () => {
    if (this.props.rows) {
      return (
        <TableHistory
          getHistory={this.props.getHistory}
          getHistoryOrdered={this.props.getHistoryOrdered}
          rows={this.props.rows}
          navigateToQA={this.props.navigateToQA}
          type={this.props.type}
          selectable={true}
          orderable={true}
          lastProcessedId={this.props.lastProcessedId}
        />
      );
    }
  };

  render() {
    return (
      <div style={{ WebkitAppRegion: 'no-drag' }}>
        {this.renderSelectDate()}
        <Card style={styles.card}>
          <Tabs value={this.state.value} onChange={this.handleChange}>
            <Tab label="Most Recent" value="last">
              {this.renderLastProcesses()}
            </Tab>
            <Tab label="History" value="history">
              <RaisedButton
                label="Refresh"
                backgroundColor={'#2196F3'}
                labelStyle={{ color: 'white' }}
                fullWidth={true}
                onClick={this.props.getHistory}
              />
              {this.renderRows()}
              {this.renderSubmit()}
            </Tab>
          </Tabs>
        </Card>
      </div>
    );
  }
}
