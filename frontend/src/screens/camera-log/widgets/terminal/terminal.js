import React, { Component } from 'react';
// import styles from './styles.css'; // eslint-disable-line
import PropTypes from 'prop-types';

const styles = {
  terminal: {
    display: 'flex',
    flex: 1,
    margin: '0 auto',
    borderRadius: '3px',
    background: 'rgba(0, 0, 0, 1)',
    overflowY: 'scroll',
    overflowX: 'scroll',
    flexDirection: 'column',
    height: 'calc(100vh - 150px)',
    width: 'calc(100vw - 75px)',
  },
  terminalOutput: {
    padding: '10px',
    lineHeight: '1.5',
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: '13px',
    fontFamily: 'Source Code Pro',
  },
};

export default class Terminal extends Component {
  static propTypes = {
    lines: PropTypes.array.isRequired,
    height: PropTypes.string,
  };

  renderLines = () => {
    return (
      <div>
        <pre style={{ margin: 0 }}>{this.props.lines.join('')}</pre>
      </div>
    );
  };

  render() {
    return (
      <div style={styles.terminal}>
        <div style={styles.terminalOutput}>{this.renderLines()}</div>
      </div>
    );
  }
}
