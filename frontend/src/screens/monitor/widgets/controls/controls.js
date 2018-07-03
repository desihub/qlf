import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Popover from '@material-ui/core/Popover';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import ConfirmDialog from '../../../../components/dialog/dialog';

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
  clearButtons: { fontSize: 12, padding: 12, minHeight: 0 },
  clearButton: { fontSize: 12, marginTop: 8 },
  checkbox: { height: 26 },
};

class Controls extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedClearDisk: [],
      confirmDialog: false,
    };
  }

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

  handleChangeCheckbox = name => {
    const { selectedClearDisk } = this.state;
    if (!selectedClearDisk.find(c => c === name)) {
      this.setState({
        selectedClearDisk: selectedClearDisk.concat(name),
      });
    } else {
      this.setState({
        selectedClearDisk: selectedClearDisk.filter(tch => tch !== name),
      });
    }
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
        <div className={classes.clearButtons}>
          <FormControl component="fieldset">
            <FormLabel component="legend">Delete Files</FormLabel>
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={this.state.selectedClearDisk.find(
                      c => c === 'raw'
                    )}
                    classes={{
                      root: classes.checkbox,
                    }}
                    onChange={() => this.handleChangeCheckbox('raw')}
                  />
                }
                label="Raw"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={this.state.selectedClearDisk.find(
                      c => c === 'reduced'
                    )}
                    classes={{
                      root: classes.checkbox,
                    }}
                    onChange={() => this.handleChangeCheckbox('reduced')}
                  />
                }
                label="Reduced"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={this.state.selectedClearDisk.find(
                      c => c === 'logs'
                    )}
                    classes={{
                      root: classes.checkbox,
                    }}
                    onChange={() => this.handleChangeCheckbox('log')}
                  />
                }
                label="Logs"
              />
            </FormGroup>
            <Button
              className={classes.clearButton}
              onMouseDown={this.confirmDeleteFiles}
              fullWidth
              variant="raised"
              disabled={this.state.selectedClearDisk.length === 0}
            >
              submit
            </Button>
          </FormControl>
        </div>
      </Popover>
    );
  };

  confirmDeleteFiles = () => {
    this.setState({
      confirmDialog: true,
      confirmDialogSubtitle: `Are sure you want to delete all ${this.state.selectedClearDisk.join(
        ', '
      )} files?`,
    });
  };

  confirmDelete = () => {
    this.state.selectedClearDisk.forEach(type => {
      this.props.socket.state.ws.send(
        `delete${type.charAt(0).toUpperCase() + type.slice(1)}`
      );
    });
    this.setState({ anchorEl: null, selectedClearDisk: [] });
  };

  closeConfirmDialog = () => {
    this.setState({ confirmDialog: false });
  };

  render() {
    return (
      <div style={styles.controls}>
        <ConfirmDialog
          title={'Confirmation'}
          subtitle={this.state.confirmDialogSubtitle}
          open={this.state.confirmDialog}
          handleClose={this.closeConfirmDialog}
          onConfirm={this.confirmDelete}
        />
        {this.renderClearPopover()}
        {this.renderStartOrStop()}
        {this.renderReset()}
        {/* {this.renderClear()} */}
      </div>
    );
  }
}

export default withStyles(styles)(Controls);
