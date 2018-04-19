import React, { Component } from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import PropTypes from 'prop-types';

const styles = {
  controls: {
    padding: '1vh',
    minWidth: '5em',
    width: '12vw',
    marginRight: '1vw',
  },
  button: { height: 'calc(1em + 2vh)' },
  buttonLabel: { fontSize: 'calc(5px + 1vh)', top: '0.5vh' },
  white: { color: 'white' },
};

export default class Controls extends Component {
  static propTypes = {
    socket: PropTypes.object,
    daemonStatus: PropTypes.string,
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
    return this.props.daemonStatus === 'Running' ? (
      <RaisedButton
        label="Stop"
        style={styles.button}
        labelStyle={{ ...styles.buttonLabel, ...styles.white }}
        backgroundColor={'#ff0000'}
        fullWidth={true}
        onMouseDown={this.stopPipeline}
      />
    ) : (
      <RaisedButton
        label="Start"
        style={styles.button}
        labelStyle={{ ...styles.buttonLabel, ...styles.white }}
        backgroundColor={'#00C853'}
        fullWidth={true}
        onMouseDown={this.startPipeline}
      />
    );
  };

  render() {
    return (
      <div style={styles.controls}>
        {this.renderStartOrStop()}
        <RaisedButton
          label="reset"
          style={styles.button}
          labelStyle={styles.buttonLabel}
          fullWidth={true}
          onMouseDown={this.resetPipeline}
        />
      </div>
    );
  }
}
