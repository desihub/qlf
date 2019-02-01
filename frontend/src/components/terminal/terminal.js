import React, { Component } from 'react';
import PropTypes from 'prop-types';

const styles = {
  terminal: {
    display: 'flex',
    flex: 1,
    margin: '0 0 0 8px',
    borderRadius: '3px',
    background: 'rgba(0, 0, 0, 1)',
    overflow: 'auto',
    flexDirection: 'column',
  },
  terminalOutput: {
    padding: '10px',
    lineHeight: '1.5',
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: '1vw',
    fontFamily: 'Source Code Pro',
    fontWeight: 'bold',
  },
};

export default class Terminal extends Component {
  static propTypes = {
    lines: PropTypes.array.isRequired,
    height: PropTypes.string,
    width: PropTypes.string,
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

    const terminalWidth = {
      width: this.props.width ? this.props.width : '100%',
    };

    return (
      <div
        style={{
          ...styles.terminal,
          ...terminalHeight,
          ...terminalWidth,
        }}
      >
        <div style={styles.terminalOutput}>{this.renderLines()}</div>
      </div>
    );
  }
}
