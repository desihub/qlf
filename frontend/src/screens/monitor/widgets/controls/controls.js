import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Popover from '@material-ui/core/Popover';
import Typography from '@material-ui/core/Typography';

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
  clearButton: { fontSize: 12, padding: 2, minHeight: 0 },
  clearButtons: { display: 'flex', flexDirection: 'column' },
};

class Controls extends Component {
  static propTypes = {
    socket: PropTypes.object,
    daemonRunning: PropTypes.bool,
    classes: PropTypes.object,
    resetMonitor: PropTypes.func.isRequired,
  };

  startPipeline = () => {
    this.props.socket.state.ws.send('startPipeline');
  };

  stopPipeline = () => {
    this.props.socket.state.ws.send('stopPipeline');
  };

  renderStartOrStop = () => {
    const { classes } = this.props;
    return this.props.daemonRunning ? (
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
      disabled={this.props.daemonRunning}
    >
      Reset
    </Button>
  );

  renderClear = () => (
    <Button
      className={this.props.classes.button}
      variant="raised"
      onMouseDown={this.handleClick}
    >
      Clear Disk
    </Button>
  );

  state = {
    anchorEl: null,
  };

  handleClick = event => {
    this.setState({
      anchorEl: event.currentTarget,
    });
  };

  handleClose = () => {
    this.setState({
      anchorEl: null,
    });
  };

  renderClearPopover = () => {
    const { anchorEl } = this.state;
    const { classes } = this.props;
    return (
      <Popover
        open={Boolean(anchorEl)}
        anchorEl={anchorEl}
        onClose={this.handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
      >
        <div>
          <Typography variant="caption">Cleaning:</Typography>
          <div className={classes.clearButtons}>
            <Button
              className={this.props.classes.clearButton}
              variant="raised"
              onMouseDown={() => this.deleteFiles('deleteAll')}
            >
              all
            </Button>
            <Button
              className={this.props.classes.clearButton}
              variant="raised"
              onMouseDown={() => this.deleteFiles('deleteRaw')}
            >
              raw
            </Button>
            <Button
              className={this.props.classes.clearButton}
              variant="raised"
              onMouseDown={() => this.deleteFiles('deleteReduced')}
            >
              reduced
            </Button>
            <Button
              className={this.props.classes.clearButton}
              variant="raised"
              onMouseDown={() => this.deleteFiles('deleteLogs')}
            >
              logs
            </Button>
            <Button
              className={this.props.classes.clearButton}
              variant="raised"
              onMouseDown={() => this.deleteFiles('')}
            >
              spectra
            </Button>
          </div>
        </div>
      </Popover>
    );
  };

  deleteFiles = type => {
    this.props.socket.state.ws.send(type);
    this.setState({ anchorEl: null });
  };

  render() {
    return (
      <div style={styles.controls}>
        {this.renderClearPopover()}
        {this.renderStartOrStop()}
        {this.renderReset()}
        {this.renderClear()}
      </div>
    );
  }
}

export default withStyles(styles)(Controls);
