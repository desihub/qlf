import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const styles = {
  controls: {
    minWidth: '5em',
    width: '12vw',
    marginLeft: '1vw',
    display: 'flex',
    alignItems: 'center',
  },
  button: { fontSize: 12, marginRight: 12, padding: 2, minHeight: 0 },
  green: { backgroundColor: 'green', color: 'white' },
  red: { backgroundColor: 'red', color: 'white' },
};

class Controls extends Component {
  static propTypes = {
    socket: PropTypes.object,
    daemonStatus: PropTypes.string,
    classes: PropTypes.object,
    resetMonitor: PropTypes.func.isRequired,
  };

  startPipeline = () => {
    this.props.socket.state.ws.send('startPipeline');
  };

  stopPipeline = () => {
    this.props.socket.state.ws.send('stopPipeline');
  };

  resetPipeline = () => {
    this.props.socket.state.ws.send('resetPipeline');
  };

  renderStartOrStop = () => {
    const { classes } = this.props;
    return this.props.daemonStatus === 'Running' ||
      this.props.daemonStatus === 'Idle' ? (
      <Button
        className={classes.button}
        classes={{ raised: classes.red }}
        variant="raised"
        onMouseDown={this.stopPipeline}
      >
        Stop
      </Button>
    ) : (
      <Button
        className={classes.button}
        classes={{ raised: classes.green }}
        variant="raised"
        onMouseDown={this.startPipeline}
      >
        Start
      </Button>
    );
  };

  renderReset = () => (
    <Button
      className={this.props.classes.button}
      variant="raised"
      onMouseDown={this.props.resetMonitor}
    >
      Reset
    </Button>
  );

  renderClear = () => (
    <Button className={this.props.classes.button} variant="raised">
      Clear Disk
    </Button>
  );

  render() {
    return (
      <div style={styles.controls}>
        {this.renderStartOrStop()}
        {this.renderReset()}
        {this.renderClear()}
      </div>
    );
  }
}

export default withStyles(styles)(Controls);
