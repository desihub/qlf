import React from 'react';
import QLFApi from '../../../../containers/offline/connection/qlf-api';
import CircularProgress from '@material-ui/core/CircularProgress';
import PropTypes from 'prop-types';

const styles = {
  config: {
    overflowX: 'auto',
    margin: '1em',
  },
};

export default class Display extends React.Component {
  static propTypes = {
    config: PropTypes.bool.isRequired,
  };

  state = {
    qlconfig: '',
    qlCalibration: '',
    loading: false,
  };

  componentWillMount() {
    if (this.props.config) {
      this.getQlConfig();
    } else {
      this.getQlCalibration();
    }
  }

  getQlConfig = async () => {
    this.setState({ loading: true });
    const qlconfig = await QLFApi.getQlConfig();
    this.setState({ qlconfig, loading: false });
  };

  getQlCalibration = async () => {
    this.setState({ loading: true });
    let qlCalibration = await QLFApi.getQlCalibration();
    if (Array.isArray(qlCalibration)) qlCalibration = qlCalibration.join('\n');
    this.setState({ qlCalibration, loading: false });
  };

  render() {
    const currentConfig = this.props.config
      ? this.state.qlconfig
      : this.state.qlCalibration;
    return this.state.loading ? (
      <CircularProgress size={50} />
    ) : (
      <pre style={styles.config}>{currentConfig}</pre>
    );
  }
}
