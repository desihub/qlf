import React from 'react';
import PropTypes from 'prop-types';
import Terminal from './widgets/terminal/terminal';
import Paper from '@material-ui/core/Paper';

const styles = {
  close: {
    float: 'right',
    cursor: 'pointer',
  },
  main: {
    margin: '16px',
    padding: '16px',
  },
};

export default class CameraLog extends React.Component {
  static propTypes = {
    cameraIndex: PropTypes.string.isRequired,
    arm: PropTypes.string.isRequired,
    lines: PropTypes.array.isRequired,
    websocketRef: PropTypes.object,
    online: PropTypes.bool,
  };

  componentDidMount() {
    this.refreshLog = setTimeout(this.getLines, 2000);
  }

  componentWillUnmount() {
    clearInterval(this.refreshLog);
  }

  getLines = () => {
    if (
      this.props.online &&
      this.props.arm &&
      this.props.cameraIndex &&
      this.props.websocketRef
    ) {
      this.props.websocketRef.state.ws.send(
        `camera:${this.props.arm}${this.props.cameraIndex}`
      );
    }
  };

  renderTitle = () => {
    return (
      <div>
        <span>{`Camera ${this.props.arm}${this.props.cameraIndex}`}</span>
      </div>
    );
  };

  render() {
    return (
      <Paper elevation={4} style={styles.main}>
        {this.renderTitle()}
        <Terminal lines={this.props.lines.reverse()} />
      </Paper>
    );
  }
}
