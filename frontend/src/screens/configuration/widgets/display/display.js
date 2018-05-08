import React from 'react';
import QLFApi from '../../../../containers/offline/connection/qlf-api';
import { CircularProgress } from 'material-ui-next/Progress';

const styles = {
  qlconfig: {
    overflowX: 'auto',
    margin: '1em',
  },
};

export default class Display extends React.Component {
  state = {
    qlconfig: '',
    loading: false,
  };

  componentWillMount() {
    this.getQlConfig();
  }

  getQlConfig = async () => {
    this.setState({ loading: true });
    const qlconfig = await QLFApi.getQlConfig();
    this.setState({ qlconfig, loading: false });
  };

  render() {
    return this.state.loading ? (
      <CircularProgress size={50} />
    ) : (
      <pre style={styles.qlconfig}>{this.state.qlconfig}</pre>
    );
  }
}
