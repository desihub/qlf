import React, { Component } from 'react';
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';
import _ from 'lodash';
import { Card } from 'material-ui/Card';
import PropTypes from 'prop-types';

const tableData = _.map(_.range(10), function() {
  return { pre: '', spec: '', fib: '', sky: '' };
});

const headerSize = 'calc(1px + 0.6vh + 0.6vw)';

const styles = {
  flex: { display: 'flex', flexDirection: 'row', alignItems: 'center' },
  leftCol: { marginRight: '1vw', marginLeft: '1vw', marginTop: '1vh' },
  rightCol: { flex: 1, marginLeft: '1vw', marginRight: '1vw' },
  singleCol: { marginTop: '2vh' },
  card: {
    borderLeft: 'solid 4px green',
    flex: '1',
    marginRight: '1vw',
  },
  arm: {
    color: '#9E9E9E',
    fontWeight: 'bold',
  },
};

export default class Stages extends Component {
  static propTypes = {
    arm: PropTypes.string.isRequired,
    openDialog: PropTypes.func.isRequired,
    status: PropTypes.array.isRequired,
    renderHeader: PropTypes.bool.isRequired,
  };

  state = {
    fixedHeader: false,
    fixedFooter: true,
    stripedRows: true,
    showRowHover: true,
    selectable: false,
    multiSelectable: false,
    enableSelectAll: false,
    deselectOnClickaway: true,
    showCheckboxes: false,
    columnHeight: '0.7vh',
    openDialog: true,
  };

  handleToggle = (event, toggled) => {
    this.setState({
      [event.target.name]: toggled,
    });
  };

  handleChange = event => {
    this.setState({ height: event.target.value });
  };

  getColor = row => {
    switch (row) {
      case 'success_stage':
        return { backgroundColor: 'green' };
      case 'processing_stage':
        return { backgroundColor: 'yellow' };
      case 'error_stage':
        return { backgroundColor: 'red' };
      default:
        return {};
    }
  };

  renderTableHeader = () => {
    if (!this.props.renderHeader) return;
    return (
      <TableHeader
        displaySelectAll={this.state.showCheckboxes}
        adjustForCheckbox={this.state.showCheckboxes}
        enableSelectAll={this.state.enableSelectAll}
      >
        <TableRow style={{ height: this.state.columnHeight }}>
          <TableHeaderColumn
            style={{
              fontSize: headerSize,
              height: this.state.columnHeight,
              whiteSpace: 'normal',
            }}
            tooltip={'Pre Processing'}
          >
            Step 1
          </TableHeaderColumn>
          <TableHeaderColumn
            style={{
              fontSize: headerSize,
              height: this.state.columnHeight,
              whiteSpace: 'normal',
            }}
            tooltip={'Spectral Extraction'}
          >
            Step 2
          </TableHeaderColumn>
          <TableHeaderColumn
            style={{
              fontSize: headerSize,
              height: this.state.columnHeight,
              whiteSpace: 'normal',
            }}
            tooltip={'Fiber Flattening'}
          >
            Step 3
          </TableHeaderColumn>
          <TableHeaderColumn
            style={{
              fontSize: headerSize,
              height: this.state.columnHeight,
              whiteSpace: 'normal',
            }}
            tooltip={'Sky Subtraction'}
          >
            Step 4
          </TableHeaderColumn>
          <TableHeaderColumn
            style={{
              fontSize: this.state.columnHeight,
              height: this.state.columnHeight,
              whiteSpace: 'normal',
              width: '1px',
            }}
          />
        </TableRow>
      </TableHeader>
    );
  };

  render() {
    let stage_status = tableData;
    if (this.props.status.length > 0) {
      stage_status = tableData.map((row, index) => {
        row.pre = this.props.status[0].camera[index];
        row.spec = this.props.status[1].camera[index];
        row.fib = this.props.status[2].camera[index];
        row.sky = this.props.status[3].camera[index];
        return row;
      });
    }

    return (
      <div>
        <Card style={styles.card}>
          <div style={styles.flex}>
            <div style={styles.leftCol}>
              <div style={styles.flex}>
                <span style={styles.arm}>{this.props.arm}</span>
              </div>
            </div>
            <div style={styles.rightCol}>
              <div style={styles.flex}>
                <Table
                  id="stages"
                  height={this.state.height}
                  width={'10px'}
                  fixedHeader={this.state.fixedHeader}
                  fixedFooter={this.state.fixedFooter}
                  selectable={this.state.selectable}
                  multiSelectable={this.state.multiSelectable}
                >
                  {this.renderTableHeader()}
                  <TableBody
                    displayRowCheckbox={this.state.showCheckboxes}
                    deselectOnClickaway={this.state.deselectOnClickaway}
                    showRowHover={this.state.showRowHover}
                    stripedRows={this.state.stripedRows}
                  >
                    {stage_status.map((row, index) => (
                      <TableRow
                        key={index}
                        style={{ height: this.state.columnHeight }}
                      >
                        <TableRowColumn
                          style={{
                            fontSize: this.state.columnHeight,
                            height: this.state.columnHeight,
                            ...this.getColor(row.pre),
                          }}
                        />
                        <TableRowColumn
                          style={{
                            fontSize: this.state.columnHeight,
                            height: this.state.columnHeight,
                            ...this.getColor(row.spec),
                          }}
                        />
                        <TableRowColumn
                          style={{
                            fontSize: this.state.columnHeight,
                            height: this.state.columnHeight,
                            ...this.getColor(row.fib),
                          }}
                        />
                        <TableRowColumn
                          style={{
                            fontSize: this.state.columnHeight,
                            height: this.state.columnHeight,
                            ...this.getColor(row.sky),
                          }}
                        />
                        <TableRowColumn
                          style={{
                            fontSize: this.state.columnHeight,
                            height: this.state.columnHeight,
                            width: '1px',
                          }}
                        >
                          <span
                            style={{ cursor: 'pointer', color: '#9E9E9E' }}
                            onClick={() =>
                              this.props.openDialog(index, this.props.arm)
                            }
                          >
                            ✚
                          </span>
                        </TableRowColumn>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>
          </div>
        </Card>
      </div>
    );
  }
}
