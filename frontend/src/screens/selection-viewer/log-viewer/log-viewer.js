import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import QlfApi from '../../../containers/offline/connection/qlf-api';
import Terminal from '../../../components/terminal/terminal';

const styles = {};

class LogViewer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      processId: undefined,
      lines: [],
    };
  }
  static propTypes = {
    spectrograph: PropTypes.array,
    arm: PropTypes.string,
    loadEnd: PropTypes.func.isRequired,
    loadStart: PropTypes.func.isRequired,
    loading: PropTypes.bool.isRequired,
  };

  componentWillMount() {
    document.title = 'Log Viewer';
    if (window.location.search.includes('process=')) {
      const processId = window.location.search.split('process=')[1];
      this.setState({
        processId,
      });
    }
  }

  componentWillReceiveProps(nextProps) {
    if (
      (this.props.arm !== nextProps.arm &&
        this.props.spectrograph.length > 0) ||
      ((this.props.spectrograph.length === 0 &&
        nextProps.spectrograph.length > 0) ||
        (this.props.spectrograph[0] !== nextProps.spectrograph[0] &&
          this.props.arm))
    ) {
      this.getLines(nextProps);
    } else if (!this.props.loading) {
      this.setState({ lines: [] });
    }
  }

  getLines = async nextProps => {
    const lines = await QlfApi.getCameraLog(
      this.state.processId,
      nextProps.arm,
      nextProps.spectrograph
    );
    if (lines && lines.lines) this.setState({ lines: lines.lines.reverse() });
    this.props.loadEnd();
  };

  render() {
    return (
      <div>
        <Terminal
          lines={this.state.lines}
          width={'calc(100vw - 280px)'}
          height={'calc(100vh - 135px)'}
        />
      </div>
    );
  }
}

export default withStyles(styles)(LogViewer);
