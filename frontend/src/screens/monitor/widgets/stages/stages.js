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
import LinearProgress from '@material-ui/core/LinearProgress';
import flavors from '../../../../flavors';

const headerSize = '1vw';

const styles = {
  flex: { display: 'flex', flexDirection: 'row', alignItems: 'center' },
  leftCol: { marginRight: '1vw', marginLeft: '1vw', marginTop: '1vh' },
  rightCol: { flex: 1, marginLeft: '1vw', marginRight: '1vw' },
  card: {
    borderLeft: 'solid 4px green',
    flex: '1',
    marginRight: '1vw',
    marginBottom: 10,
  },
  arm: {
    color: '#9E9E9E',
    fontWeight: 'bold',
    fontSize: '1.2vw',
  },
  header: {
    fontSize: headerSize,
    height: 0,
    padding: 0,
    whiteSpace: 'normal',
    paddingRight: '0px',
    textAlign: 'center',
  },
  loading: {
    height: '100%',
  },
  barColorPrimary: {
    backgroundColor: 'gray',
  },
  colorPrimary: {
    backgroundColor: 'lightgray',
  },
  tooltipText: {
    fontSize: '1.5vh',
  },
};

class Stages extends Component {
  static propTypes = {
    arm: PropTypes.string.isRequired,
    openDialog: PropTypes.func.isRequired,
    status: PropTypes.array.isRequired,
    renderHeader: PropTypes.bool.isRequired,
    classes: PropTypes.object,
    pipelineRunning: PropTypes.string,
    flavor: PropTypes.string,
  };

  state = {
    columnHeight: 0,
    openDialog: true,
    completed: 0,
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
        return { backgroundColor: 'green', padding: '0.5vh' };
      case 'processing_stage':
        // return { backgroundColor: 'blue', padding: 4 };
        return {
          padding: 0,
        };
      case 'error_stage':
        return { backgroundColor: 'red', padding: '0.5vh' };
      default:
        return { padding: '0.5vh' };
    }
  };

  renderTableHeader = flavor => {
    return (
      <TableHead>
        <TableRow style={{ height: this.state.columnHeight }}>
          {flavors[flavor].step_list.map((step, idx) => {
            return (
              <Tooltip
                key={`stageHeader${idx}`}
                title={step.display_name}
                placement="bottom"
                classes={{ tooltip: this.props.classes.tooltipText }}
              >
                <TableCell style={styles.header}>Step {idx + 1}</TableCell>
              </Tooltip>
            );
          })}
        </TableRow>
      </TableHead>
    );
  };

  timer = null;

  componentDidMount() {
    this.timer = setInterval(this.progress, 2000);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  progress = () => {
    const { completed } = this.state;
    if (this.props.pipelineRunning !== 'Running') return;
    if (completed === 100) {
      this.setState({ completed: 0 });
    } else {
      const diff = 22;
      this.setState({ completed: Math.min(completed + diff, 100) });
    }
  };

  render() {
    const flavor = this.props.flavor ? this.props.flavor : 'science';
    const flavorStages = flavors[flavor].step_list.map(step => step.name);

    const stage_status = _.map(_.range(10), function() {
      const stage = {};
      flavorStages.map(stg => {
        stage[stg] = '';
        return null;
      });
      return stage;
    });

    if (this.props.status.length > 0) {
      this.props.status.map(row => {
        const index = Object.keys(row)[0];
        flavorStages.map((stg, idx) => {
          stage_status[index][stg] = row[index][idx];
          return null;
        });
        return null;
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
                  {this.renderTableHeader(flavor)}
                  <TableBody>
                    {stage_status.map((row, index) => (
                      <Tooltip
                        key={index}
                        title={`Camera ${this.props.arm}${index}`}
                        placement="top"
                        classes={{ tooltip: this.props.classes.tooltipText }}
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
                          {flavorStages.map(stg => {
                            return (
                              <TableCell
                                key={stg}
                                style={{
                                  fontSize: 0,
                                  height: 0,
                                  padding: 0,
                                  ...this.getColor(row[stg]),
                                }}
                              >
                                {row[stg] === 'processing_stage' ? (
                                  <LinearProgress
                                    style={styles.loading}
                                    variant="determinate"
                                    value={this.state.completed}
                                    classes={{
                                      barColorPrimary: this.props.classes
                                        .barColorPrimary,
                                      colorPrimary: this.props.classes
                                        .colorPrimary,
                                    }}
                                  />
                                ) : null}
                              </TableCell>
                            );
                          })}
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
