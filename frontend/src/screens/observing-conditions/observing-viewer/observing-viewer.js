import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import FormLabel from '@material-ui/core/FormLabel';

const apiUrl = process.env.REACT_APP_API;

const styles = {
  iframe: {
    height: 'calc(100vh - 215px)',
    width: 'calc(100vw - 280px)',
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

class ObservingViewer extends React.Component {
  static propTypes = {
    plot: PropTypes.string,
    arm: PropTypes.string,
    amp: PropTypes.string,
    spectrograph: PropTypes.array,
    yaxis: PropTypes.string,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    classes: PropTypes.object,
    loadEnd: PropTypes.func.isRequired,
  };

  componentDidMount() {
    document.title = 'Observing Conditions';
    if (window.location.pathname === '/observing-conditions') {
      if (window.location.search.includes('process=')) {
        this.setState({
          processId: window.location.search.split('process=')[1],
        });
      }
    }
  }

  formatDate = date => {
    return date.split('T')[0].replace(/-/g, '');
  };

  renderImage = () => {
    const { classes } = this.props;
    let url = '';

    if (
      this.props.plot === 'timeseries' &&
      this.props.yaxis !== '' &&
      this.props.startDate !== '' &&
      this.props.arm !== '' &&
      this.props.spectrograph.length !== 0 &&
      this.props.endDate !== ''
    )
      url = `${apiUrl}dashboard/load_series/?plot=${this.props.plot}&yaxis=${
        this.props.yaxis
      }&amp=${this.props.amp}&start=${this.formatDate(
        this.props.startDate
      )}&end=${this.formatDate(this.props.endDate)}&camera=${this.props.arm}${
        this.props.spectrograph[0]
      }`;

    if (url !== '')
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
    return (
      <div className={classes.preview}>
        <FormLabel component="legend">Preview:</FormLabel>
        {this.renderImage()}
      </div>
    );
  }
}

export default withStyles(styles)(ObservingViewer);
