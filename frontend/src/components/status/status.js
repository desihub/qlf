import React, { Component } from 'react';
import Cards from '../card/card';
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
    processId: PropTypes.number,
  };

  render() {
    const mjd = parseFloat(this.props.mjd)
      ? parseFloat(this.props.mjd).toFixed(5)
      : '';
    const processId = this.props.processId
      ? this.props.processId.toString()
      : '';
    return (
      <div style={{ ...styles.container }}>
        {this.props.daemonStatus ? (
          <Cards title={'Status'} subtitle={this.props.daemonStatus} />
        ) : null}
        <Cards title={'Process Id'} subtitle={processId} />
        <Cards title={'Exposure Id'} subtitle={this.props.exposure} />
        <Cards title={'MJD'} subtitle={mjd} />
        <Cards title={'Date'} subtitle={this.props.date} />
      </div>
    );
  }
}
