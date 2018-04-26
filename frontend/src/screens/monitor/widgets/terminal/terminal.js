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
    flexDirection: 'column',
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
    const terminalHeight = {
      height: this.props.height ? this.props.height : '300px',
    };

    return (
      <div style={{ ...styles.terminal, ...terminalHeight }}>
        <div style={styles.terminalOutput}>{this.renderLines()}</div>
      </div>
    );
  }
}
