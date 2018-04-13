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
    time: PropTypes.string,
  };

  render() {
    const mjd = parseFloat(this.props.mjd)
      ? parseFloat(this.props.mjd).toFixed(5)
      : '';
    return (
      <div style={this.props.layout}>
        <Cards title={'Status'} subtitle={this.props.daemonStatus} />
        <Cards title={'Exposure Id'} subtitle={this.props.exposure} />
        <Cards title={'MJD'} subtitle={mjd} />
        <Cards title={'Date'} subtitle={this.props.date} />
        <Cards title={'Time'} subtitle={this.props.time} />
      </div>
    );
  }
}
