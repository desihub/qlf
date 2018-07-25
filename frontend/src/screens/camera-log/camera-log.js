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
    cameraIndex: PropTypes.string,
    arm: PropTypes.string,
    lines: PropTypes.array.isRequired,
    getLines: PropTypes.func.isRequired,
    online: PropTypes.bool,
  };

  componentDidMount() {
    this.refreshLog = setTimeout(this.props.getLines, 2000);
  }

  componentWillUnmount() {
    clearInterval(this.refreshLog);
  }

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
