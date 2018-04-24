import React, { Component } from 'react';
import { Table, TableBody } from 'material-ui/Table';
import Proptypes from 'prop-types';
import { Card } from 'material-ui/Card';
import HistoryHeader from './history-header/history-header';
import HistoryData from './history-data/history-data';
import RaisedButton from 'material-ui/RaisedButton';

const styles = {
  card: {
    borderLeft: 'solid 4px teal',
    flex: '1',
    height: '90%',
    margin: '1em',
  },
};

export default class TableHistory extends Component {
  static propTypes = {
    getHistory: Proptypes.func.isRequired,
    getHistoryOrdered: Proptypes.func.isRequired,
    rows: Proptypes.array.isRequired,
    navigateToQA: Proptypes.func.isRequired,
    lastProcess: Proptypes.number,
    type: Proptypes.string.isRequired,
  };

  state = {
    rows: undefined,
    asc: undefined,
    ordering: undefined,
  };

  componentWillMount() {
    this.props.getHistory();
  }

  getHistoryOrdered = async ordering => {
    const order = this.state.asc ? ordering : `-${ordering}`;
    this.setState({
      rows: await this.props.getHistoryOrdered(order),
      asc: !this.state.asc,
      ordering,
    });
  };

  selectProcessQA = pk => {
    this.props.navigateToQA(pk);
  };

  renderBody = () => {
    const isProcessHistory = this.props.type === 'process';
    return (
      <TableBody showRowHover={true} displayRowCheckbox={!isProcessHistory}>
        {this.props.rows.map((row, id) => {
          const processId = isProcessHistory
            ? row.pk
            : row.last_exposure_process_id;
          return (
            <HistoryData
              key={id}
              processId={processId}
              lastProcess={this.props.lastProcess}
              row={row}
              selectProcessQA={this.selectProcessQA}
              type={this.props.type}
            />
          );
        })}
      </TableBody>
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

  render() {
    const isProcessHistory = this.props.type === 'process';
    return (
      <Card style={styles.card}>
        <Table
          fixedHeader={false}
          style={{ width: 'auto', tableLayout: 'auto' }}
          bodyStyle={{ overflow: 'visible' }}
          selectable={!isProcessHistory}
          multiSelectable={true}
        >
          <HistoryHeader
            getHistoryOrdered={this.getHistoryOrdered}
            type={this.props.type}
            asc={this.state.asc}
            ordering={this.state.ordering}
          />
          {this.renderBody()}
        </Table>
        {this.renderSubmit()}
      </Card>
    );
  }
}
