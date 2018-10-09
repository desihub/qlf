import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';

const apiUrl = process.env.REACT_APP_API;

const styles = {
  iframe: {
    height: 'calc(100vh - 135px)',
    width: 'calc(100vw - 220px)',
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

class GlobalViewer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      processId: null,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    loadEnd: PropTypes.func.isRequired,
    loadStart: PropTypes.func.isRequired,
    screen: PropTypes.string,
    arm: PropTypes.string,
  };

  componentWillMount() {
    switch (window.location.pathname) {
      case '/fiber-viewer':
        document.title = 'Fiber Viewer';
        break;
      case '/focus-viewer':
        document.title = 'Focus Viewer';
        break;
      case '/snr-viewer':
        document.title = 'SNR Viewer';
        break;
      default:
        document.title = 'Global Viewer';
    }

    if (window.location.search.includes('process=')) {
      this.setState({
        processId: window.location.search.split('process=')[1],
      });
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.arm && nextProps.arm !== this.props.arm) {
      this.props.loadStart();
    }
  }

  renderImage = () => {
    const { classes } = this.props;
    const url = `${apiUrl}dashboard/load_qa/?qa=${
      this.props.screen
    }&process_id=${this.state.processId}&arm=${this.props.arm}`;

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

export default withStyles(styles)(GlobalViewer);
