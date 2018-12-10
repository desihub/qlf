import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';

const apiUrl =
  process.env.NODE_ENV !== 'development'
    ? window.origin + '/'
    : process.env.REACT_APP_API;

const styles = {
  iframe: {
    height: 'calc(100vh - 135px)',
    width: 'calc(100vw - 64px - 12vw)',
  },
  preview: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    float: 'right',
  },
  spectrographLabel: {
    paddingBottom: 10,
  },
  main: {
    margin: '16px',
    padding: '16px',
  },
};

class SpectraViewer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      processId: null,
      screen: 'spectra',
      fiber: '',
      spectrograph: '',
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    loadEnd: PropTypes.func.isRequired,
    loadStart: PropTypes.func.isRequired,
    arm: PropTypes.string,
  };

  componentWillMount() {
    document.title = 'Spectra Viewer';
    window.addEventListener('message', this.handleIframeMessage, false);
    if (window.location.search.includes('process=')) {
      this.setState({
        processId: window.location.search.split('process=')[1],
      });
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.arm === '') {
      this.setState({
        screen: 'spectra',
        fiber: '',
        spectrograph: '',
      });
    }
  }

  handleIframeMessage = message => {
    if (message.data['fiber'] && message.data['camera']) {
      this.setState({
        screen: 'spectra_fib',
        spectrograph: message.data['camera'][1],
        fiber: message.data['fiber'],
      });
    }

    if (message.data['back']) {
      this.setState({
        screen: 'spectra',
      });
    }
  };

  renderImage = () => {
    const { classes } = this.props;
    const url = `${apiUrl}dashboard/load_spectra/?spectra=${
      this.state.screen
    }&process_id=${this.state.processId}&arm=${this.props.arm}&spectrograph=${
      this.state.spectrograph
    }&fiber=${this.state.fiber}`;

    if (this.props.arm)
      return (
        <iframe
          title="image-modal"
          className={classes.iframe}
          frameBorder="0"
          src={url}
          onLoad={this.props.loadEnd}
        />
      );
  };

  render() {
    const { classes } = this.props;
    return <div className={classes.preview}>{this.renderImage()}</div>;
  }
}

export default withStyles(styles)(SpectraViewer);
