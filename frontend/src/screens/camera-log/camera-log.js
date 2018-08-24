import React from 'react';
import PropTypes from 'prop-types';
import Terminal from '../../components/terminal/terminal';
import Paper from '@material-ui/core/Paper';

const styles = {
  close: {
    float: 'right',
    cursor: 'pointer',
  },
  main: {
    width: 'calc(100vw - 64px)',
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
    setTimeout(this.props.getLines, 2000);
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
        <Terminal
          height={'calc(100vh - 150px)'}
          lines={this.props.lines.reverse()}
        />
      </Paper>
    );
  }
}
