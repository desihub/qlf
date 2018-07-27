import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';

const apiUrl = process.env.REACT_APP_API;

const styles = {
  iframe: {
    height: 'calc(100vh - 135px)',
    width: '70vw',
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

class FiberViewer extends React.Component {
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
  };

  componentWillMount() {
    document.title = 'Fiber Viewer';
    if (window.location.pathname === '/fiber-viewer') {
      if (window.location.search.includes('process=')) {
        this.setState(
          {
            processId: window.location.search.split('process=')[1],
          },
          this.props.loadStart
        );
      }
    }
  }

  renderImage = () => {
    const { classes } = this.props;
    const url = `${apiUrl}dashboard/load_qa/?qa=globalfiber&process_id=${
      this.state.processId
    }`;

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

export default withStyles(styles)(FiberViewer);
