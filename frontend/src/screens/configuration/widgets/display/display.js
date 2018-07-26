import React from 'react';
import QLFApi from '../../../../containers/offline/connection/qlf-api';
import CircularProgress from '@material-ui/core/CircularProgress';
import PropTypes from 'prop-types';

const styles = {
  config: {
    margin: '1em',
  },
};

export default class Display extends React.Component {
  static propTypes = {
    config: PropTypes.string.isRequired,
  };

  state = {
    qlconfig: '',
    loading: false,
  };

  componentWillMount() {
    this.getQlConfig();
  }

  getQlConfig = async () => {
    this.setState({ loading: true });
    let qlconfig = await QLFApi.getQlConfig(this.props.config);
    if (Array.isArray(qlconfig)) qlconfig = qlconfig.join('\n');
    this.setState({ qlconfig, loading: false });
  };

  render() {
    const currentConfig = this.state.qlconfig;
    return this.state.loading ? (
      <CircularProgress size={50} />
    ) : (
      <pre style={styles.config}>{currentConfig}</pre>
    );
  }
}
