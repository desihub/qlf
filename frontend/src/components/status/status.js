import React, { Component } from 'react';
import Cards from '../card/card';
import PropTypes from 'prop-types';

const styles = {
  container: {
    flex: 1,
    display: 'flex',
  },
};

export default class QAStatus extends Component {
  static propTypes = {
    exposure: PropTypes.string.isRequired,
    mjd: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired,
  };

  render() {
    const mjd = parseFloat(this.props.mjd)
      ? parseFloat(this.props.mjd).toFixed(5)
      : '';
    return (
      <div style={{ ...styles.container }}>
        <Cards title={'Exposure Id'} subtitle={this.props.exposure} />
        <Cards title={'MJD'} subtitle={mjd} />
        <Cards title={'Date'} subtitle={this.props.date} />
        <Cards title={'Time'} subtitle={this.props.time} />
      </div>
    );
  }
}
