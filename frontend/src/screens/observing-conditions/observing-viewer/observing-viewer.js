import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const apiUrl =
  process.env.NODE_ENV !== 'development'
    ? window.origin + '/'
    : process.env.REACT_APP_API;

const styles = {
  iframe: {
    height: 'calc(100vh - 180px)',
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

class ObservingViewer extends React.Component {
  static propTypes = {
    plot: PropTypes.string,
    arm: PropTypes.string,
    amp: PropTypes.string,
    spectrograph: PropTypes.array,
    yaxis: PropTypes.string,
    xaxis: PropTypes.string,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    classes: PropTypes.object,
    datashader: PropTypes.bool,
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
    const endpoint = this.props.datashader
      ? `${this.props.plot}/?`
      : `dashboard/load_series/?plot=${this.props.plot}&`;

    if (
      this.props.plot === 'timeseries' &&
      this.props.yaxis !== '' &&
      this.props.startDate !== '' &&
      this.props.arm !== '' &&
      this.props.spectrograph.length !== 0 &&
      this.props.endDate !== ''
    )
      url = `${apiUrl}${endpoint}yaxis=${
        this.props.yaxis
      }&start=${this.formatDate(this.props.startDate)}&end=${this.formatDate(
        this.props.endDate
      )}&camera=${this.props.arm}${this.props.spectrograph[0]}&datashade=${
        this.props.datashader
      }`;
    else {
      if (
        this.props.plot === 'regression' &&
        this.props.yaxis !== '' &&
        this.props.xaxis !== '' &&
        this.props.startDate !== '' &&
        this.props.arm !== '' &&
        this.props.spectrograph.length !== 0 &&
        this.props.endDate !== ''
      )
        url = `${apiUrl}${endpoint}yaxis=${this.props.yaxis}&xaxis=${
          this.props.xaxis
        }&amp=${this.props.amp}&start=${this.formatDate(
          this.props.startDate
        )}&end=${this.formatDate(this.props.endDate)}&camera=${this.props.arm}${
          this.props.spectrograph[0]
        }&datashade=${this.props.datashader}`;
    }

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
    return <div className={classes.preview}>{this.renderImage()}</div>;
  }
}

export default withStyles(styles)(ObservingViewer);
