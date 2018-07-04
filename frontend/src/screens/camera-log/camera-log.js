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

  renderTitle = () => {
    return (
      <div>
        <span>{`Camera ${this.props.arm}${this.props.cameraIndex}`}</span>
      </div>
    );
  };

  render() {
    return (
      <div>
        <Paper elevation={4} style={styles.main}>
          {this.renderTitle()}
          <Terminal lines={this.props.lines} />
        </Paper>
      </div>
    );
  }
}
