import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

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

class TrendViewer extends React.Component {
  static propTypes = {
    arm: PropTypes.string,
    spectrograph: PropTypes.array,
    amp: PropTypes.array,
    plot: PropTypes.string,
    xaxis: PropTypes.string,
    yaxis: PropTypes.string,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    classes: PropTypes.object,
    loadEnd: PropTypes.func.isRequired,
    datashader: PropTypes.bool,
  };

  componentDidMount() {
    document.title = 'Trend Analysis';
    if (window.location.pathname === '/trend-analysis') {
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
      this.props.amp.length !== 0 &&
      this.props.arm !== '' &&
      this.props.spectrograph.length !== 0 &&
      this.props.startDate !== '' &&
      this.props.endDate !== ''
    )
      url = `${apiUrl}${endpoint}yaxis=${
        this.props.yaxis
      }&amp=${this.props.amp.join(',')}&start=${this.formatDate(
        this.props.startDate
      )}&end=${this.formatDate(this.props.endDate)}&camera=${this.props.arm}${
        this.props.spectrograph[0]
      }&datashade=${String(this.props.datashader)}`;
    // else if (
    //   this.props.plot === 'regression' &&
    //   this.props.xaxis !== '' &&
    //   this.props.yaxis !== '' &&
    //   this.props.amp !== '' &&
    //   this.props.startDate !== '' &&
    //   this.props.endDate !== ''
    // )
    //   url = `${apiUrl}dashboard/load_series/?plot=${this.props.plot}&xaxis=${
    //     this.props.xaxis
    //   }${this.props.amp}&yaxis=${this.props.yaxis}${this.props.amp}`;

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

export default withStyles(styles)(TrendViewer);
