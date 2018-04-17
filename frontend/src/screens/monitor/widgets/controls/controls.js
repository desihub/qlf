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
  buttonStyle: { padding: '1vh 0vw 0vw 0vh' },
  buttonLabel: { fontSize: 'calc(5px + 1vh)' },
  white: { color: 'white' },
};

export default class Controls extends Component {
  static propTypes = {
    socket: PropTypes.object,
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

  render() {
    return (
      <div style={styles.controls}>
        <RaisedButton
          label="Start"
          style={styles.button}
          buttonStyle={styles.buttonStyle}
          labelStyle={{ ...styles.buttonLabel, ...styles.white }}
          backgroundColor={'#00C853'}
          fullWidth={true}
          onMouseDown={this.startPipeline}
        />
        <RaisedButton
          label="Stop"
          style={styles.button}
          buttonStyle={styles.buttonStyle}
          labelStyle={{ ...styles.buttonLabel, ...styles.white }}
          backgroundColor={'#ff0000'}
          fullWidth={true}
          onMouseDown={this.stopPipeline}
        />
        <RaisedButton
          label="reset"
          buttonStyle={styles.buttonStyle}
          style={styles.button}
          labelStyle={styles.buttonLabel}
          fullWidth={true}
          onMouseDown={this.resetPipeline}
        />
      </div>
    );
  }
}
