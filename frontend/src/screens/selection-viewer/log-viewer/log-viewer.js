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
      lines: [],
    };
  }
  static propTypes = {
    spectrograph: PropTypes.array,
    arm: PropTypes.string,
    loadEnd: PropTypes.func.isRequired,
    loadStart: PropTypes.func.isRequired,
  };

  componentWillMount() {
    document.title = 'Log Viewer';
    if (window.location.search.includes('process=')) {
      const processId = window.location.search.split('process=')[1];
      this.getLines(processId);
    }
  }

  getLines = async processId => {
    const lines = await QlfApi.getCameraLog(
      processId,
      this.props.arm,
      this.props.spectrograph
    );
    if (lines && lines.lines) this.setState({ lines: lines.lines.reverse() });
    else this.setState({ lines: ['Logs not found'] });
    this.props.loadEnd();
  };

  render() {
    return (
      <div>
        <Terminal
          lines={this.state.lines}
          width={'calc(100vw - 72px - 12vw)'}
          height={'calc(100vh - 135px)'}
        />
      </div>
    );
  }
}

export default withStyles(styles)(LogViewer);
