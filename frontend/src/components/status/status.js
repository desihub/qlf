import React, { Component } from 'react';
import Card from '../card/card';
import PropTypes from 'prop-types';

const styles = {
  container: {
    flex: 1,
    display: 'flex',
  },
};

export default class Status extends Component {
  static propTypes = {
    daemonStatus: PropTypes.string,
    exposure: PropTypes.string.isRequired,
    mjd: PropTypes.string,
    date: PropTypes.string,
    processId: PropTypes.string,
  };

  render() {
    const mjd = parseFloat(this.props.mjd)
      ? parseFloat(this.props.mjd).toFixed(3)
      : '';
    const processId = this.props.processId
      ? this.props.processId.toString()
      : '';
    return (
      <div style={{ ...styles.container }}>
        {this.props.daemonStatus ? (
          <Card title={`Status: ${this.props.daemonStatus}`} />
        ) : null}
        <Card title={`Process Id: ${processId}`} />
        <Card title={`Exposure Id: ${this.props.exposure}`} />
        <Card title={`MJD: ${mjd}`} />
        <Card title={`Date: ${this.props.date}`} />
      </div>
    );
  }
}
