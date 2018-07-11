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
    pipelineRunning: PropTypes.string,
    exposureId: PropTypes.string.isRequired,
    mjd: PropTypes.string,
    date: PropTypes.string,
    flavor: PropTypes.string,
    processId: PropTypes.string,
  };

  render() {
    const mjd = parseFloat(this.props.mjd)
      ? parseFloat(this.props.mjd).toFixed(3)
      : '';
    const processId =
      this.props.processId && !this.props.processId.includes('-')
        ? this.props.processId
        : '';
    return (
      <div style={{ ...styles.container }}>
        {this.props.pipelineRunning ? (
          <Card title={`Status: ${this.props.pipelineRunning}`} />
        ) : null}
        <Card title={`Flavor: ${this.props.flavor}`} />
        <Card title={`Process Id: ${processId}`} />
        <Card title={`Exposure Id: ${this.props.exposureId}`} />
        <Card title={`MJD: ${mjd}`} />
        <Card title={`Date: ${this.props.date}`} />
      </div>
    );
  }
}
