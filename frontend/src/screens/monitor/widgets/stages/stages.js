import React, { Component } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import _ from 'lodash';
import { Card } from 'material-ui/Card';
import PropTypes from 'prop-types';
import Tooltip from '@material-ui/core/Tooltip';
import { withStyles } from '@material-ui/core/styles';

const headerSize = '11px';

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
  header: {
    fontSize: headerSize,
    height: 1,
    whiteSpace: 'normal',
    paddingRight: '0px',
    textAlign: 'center',
  },
};

class Stages extends Component {
  static propTypes = {
    arm: PropTypes.string.isRequired,
    openDialog: PropTypes.func.isRequired,
    status: PropTypes.array.isRequired,
    renderHeader: PropTypes.bool.isRequired,
    classes: PropTypes.object,
  };

  state = {
    columnHeight: 1,
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
      <TableHead>
        <TableRow style={{ height: this.state.columnHeight }}>
          <Tooltip title={'Pre Processing'} placement="bottom">
            <TableCell style={styles.header}>Step 1</TableCell>
          </Tooltip>
          <Tooltip title={'Spectral Extraction'} placement="bottom">
            <TableCell style={styles.header}>Step 2</TableCell>
          </Tooltip>
          <Tooltip title={'Fiber Flattening'} placement="bottom">
            <TableCell style={styles.header}>Step 3</TableCell>
          </Tooltip>
          <Tooltip title={'Sky Subtraction'} placement="bottom">
            <TableCell style={styles.header}>Step 4</TableCell>
          </Tooltip>
        </TableRow>
      </TableHead>
    );
  };

  render() {
    let stage_status = _.map(_.range(10), function() {
      return { pre: '', spec: '', fib: '', sky: '' };
    });
    if (this.props.status.length > 0) {
      stage_status = stage_status.map((row, index) => {
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
                <Table id="stages" height={this.state.height} width={'10px'}>
                  {this.renderTableHeader()}
                  <TableBody>
                    {stage_status.map((row, index) => (
                      <Tooltip
                        key={index}
                        title={`Camera ${this.props.arm}${index}`}
                        placement="top"
                      >
                        <TableRow
                          hover
                          style={{
                            height: this.state.columnHeight,
                            cursor: 'pointer',
                          }}
                          onClick={() =>
                            this.props.openDialog(index, this.props.arm)
                          }
                        >
                          <TableCell
                            style={{
                              fontSize: this.state.columnHeight,
                              height: this.state.columnHeight,
                              ...this.getColor(row.pre),
                            }}
                          />
                          <TableCell
                            style={{
                              fontSize: this.state.columnHeight,
                              height: this.state.columnHeight,
                              ...this.getColor(row.spec),
                            }}
                          />
                          <TableCell
                            style={{
                              fontSize: this.state.columnHeight,
                              height: this.state.columnHeight,
                              ...this.getColor(row.fib),
                            }}
                          />
                          <TableCell
                            style={{
                              fontSize: this.state.columnHeight,
                              height: this.state.columnHeight,
                              ...this.getColor(row.sky),
                            }}
                          />
                        </TableRow>
                      </Tooltip>
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

export default withStyles(styles)(Stages);
