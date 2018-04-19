import React, { Component } from 'react';
import Cards from '../../../../components/card/card';
import PropTypes from 'prop-types';

export default class Status extends Component {
  static propTypes = {
    layout: PropTypes.object.isRequired,
    daemonStatus: PropTypes.string.isRequired,
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
      <div style={this.props.layout}>
        <Cards title={'Status'} subtitle={this.props.daemonStatus} />
        <Cards title={'Process Id'} subtitle={processId} />
        <Cards title={'Exposure Id'} subtitle={this.props.exposure} />
        <Cards title={'MJD'} subtitle={mjd} />
        <Cards title={'Date'} subtitle={this.props.date} />
      </div>
    );
  }
}
