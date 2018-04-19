import React from 'react';
import Card from '../card/card';
import PropTypes from 'prop-types';

const styles = {
  singleCol: {
    flex: 1,
    display: 'flex',
    margin: '1vw',
  },
  linkStyle: { textDecoration: 'none', flex: 1 },
};

export default class Home extends React.Component {
  static propTypes = {
    updateUrl: PropTypes.func.isRequired,
  };

  state = {
    layout: { flexDirection: 'row' },
  };

  navigateTo = route => {
    this.props.updateUrl(route);
    window.open(route);
  };

  componentDidMount() {
    this.updateWindowDimensions();
    window.addEventListener('resize', this.updateWindowDimensions);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updateWindowDimensions);
  }

  updateWindowDimensions = () => {
    this.setState({
      layout: {
        flexDirection: window.innerWidth < 300 ? 'row' : 'row',
      },
    });
  };

  render() {
    return (
      <div>
        <div style={{ ...styles.singleCol, ...this.state.layout }}>
          <a
            style={styles.linkStyle}
            onClick={() => this.navigateTo('/monitor-realtime')}
          >
            <Card
              icon="Web"
              title="Pipeline Monitor"
              subtitle="Control and monitor the execution of the Quick Look pipeline"
            />
          </a>
          <a
            style={styles.linkStyle}
            onClick={() => this.navigateTo('/qa-realtime')}
          >
            <Card
              icon="RemoveRedEye"
              title="QA"
              subtitle="Monitor QA metrics and provide access to diagnostic plots"
            />
          </a>
          <a
            style={styles.linkStyle}
            onClick={() => this.navigateTo('/processing-history')}
          >
            <Card
              icon="AddToQueue"
              title="Processing History"
              subtitle="List exposures that have been processed"
            />
          </a>
        </div>
        <div style={{ ...styles.singleCol, ...this.state.layout }}>
          <a style={styles.linkStyle} onClick={() => this.navigateTo('/')}>
            <Card
              icon="History"
              title="Observing History"
              subtitle="Display time series plots for QA metrics, list of exposures and observed targets for the current night of for a range of nights"
            />
          </a>
          <a style={styles.linkStyle} onClick={() => this.navigateTo('/')}>
            <Card
              icon="BrightnessMedium"
              title="Afternoon Planning"
              subtitle="Browse QA results for exposures processed by the offline pipeline at NERSC"
            />
          </a>
          <a style={styles.linkStyle} onClick={() => this.navigateTo('/')}>
            <Card
              icon="TrendingUp"
              title="Trend Analysis"
              subtitle="Simple plots using quantities stored in the database"
            />
          </a>
        </div>
        <div style={{ ...styles.singleCol, ...this.state.layout }}>
          <a style={styles.linkStyle} onClick={() => this.navigateTo('/')}>
            <Card
              icon="Cloud"
              title="Sky Conditions"
              subtitle="Display sky conditions such as atmospheric transparency, seeing, and sky background from the GFA camera"
            />
          </a>
          <a style={styles.linkStyle} onClick={() => this.navigateTo('/')}>
            <Card
              icon="Assignment"
              title="Survey Reports"
              subtitle="Show the overall progress and performance of survey"
            />
          </a>
          <a style={styles.linkStyle} onClick={() => this.navigateTo('/')}>
            <Card
              icon="ViewModule"
              title="Configuration"
              subtitle="Configuration of initial settings for execution"
            />
          </a>
        </div>
      </div>
    );
  }
}
