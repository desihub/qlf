import React from 'react';
import Form from './widgets/form/form';
import Display from './widgets/display/display';
import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    margin: '1em',
    overflow: 'auto',
    height: 'calc(100vh - 66px - 2em)',
    width: 'calc(100vw - 2em)',
    fontSize: '1.2vw',
  },
  tabItem: {
    fontSize: '1.2vw',
  },
  tabsH: {
    minHeight: '4.8vh',
  },
  tabWH: {
    minWidth: '11vw',
    minHeight: '4.8vh',
  },
};

class Configuration extends React.Component {
  static propTypes = {
    daemonRunning: PropTypes.bool.isRequired,
    classes: PropTypes.object.isRequired,
  };

  state = {
    tab: 0,
    qlTab: 0,
    qlScienceTab: 0,
    qlCalibrationTab: 0,
  };

  componentDidMount() {
    document.title = 'Configuration';
  }

  handleTabChange = (evt, tab) => {
    this.setState({ tab });
  };

  handleQlTabChange = (evt, qlTab) => {
    this.setState({ qlTab });
  };

  handleQlScienceTabChange = (evt, qlScienceTab) => {
    this.setState({ qlScienceTab });
  };

  handleQlCalibrationTabChange = (evt, qlCalibrationTab) => {
    this.setState({ qlCalibrationTab });
  };

  renderScience = () => {
    const { qlScienceTab, qlTab } = this.state;
    const { classes } = this.props;
    if (qlTab !== 0) return null;
    return (
      <div>
        <Tabs
          value={qlScienceTab}
          onChange={this.handleQlScienceTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
          style={styles.tabsH}
        >
          <Tab
            label="Dark"
            value={0}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="Bright"
            value={1}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="Gray"
            value={2}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
        </Tabs>
        {qlScienceTab === 0 ? <Display config={'science'} /> : null}
        {qlScienceTab === 1 ? <Display config={'science'} /> : null}
        {qlScienceTab === 2 ? <Display config={'science'} /> : null}
      </div>
    );
  };

  renderCalibration = () => {
    const { qlCalibrationTab, qlTab } = this.state;
    const { classes } = this.props;
    if (qlTab !== 1) return null;
    return (
      <div>
        <Tabs
          value={qlCalibrationTab}
          onChange={this.handleQlCalibrationTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
          style={styles.tabsH}
        >
          <Tab
            label="Flat"
            value={0}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="Dark Current"
            value={1}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="Bias"
            value={2}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="ARC"
            value={3}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
        </Tabs>
        {qlCalibrationTab === 0 ? <Display config={'flat'} /> : null}
        {qlCalibrationTab === 1 ? <Display config={'darkcurrent'} /> : null}
        {qlCalibrationTab === 2 ? <Display config={'bias'} /> : null}
        {qlCalibrationTab === 3 ? <Display config={'arc'} /> : null}
      </div>
    );
  };

  renderTabs = () => {
    const { qlTab } = this.state;
    const { classes } = this.props;
    return (
      <div>
        <Tabs
          value={qlTab}
          onChange={this.handleQlTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
          style={styles.tabsH}
        >
          <Tab
            label="SCIENCE"
            value={0}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
          <Tab
            label="Calibration"
            value={1}
            classes={{ root: classes.tabWH, label: classes.tabItem }}
          />
        </Tabs>
        {qlTab === 0 ? this.renderScience() : null}
        {qlTab === 1 ? this.renderCalibration() : null}
      </div>
    );
  };

  render() {
    const { tab } = this.state;
    const { classes } = this.props;
    return (
      <div>
        <Paper style={styles.container} elevation={4}>
          <Tabs
            value={tab}
            onChange={this.handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            fullWidth
            centered
            style={styles.tabsH}
          >
            <Tab
              label="QLF"
              value={0}
              classes={{ root: classes.tabWH, label: classes.tabItem }}
            />
            <Tab
              label="QL"
              value={1}
              classes={{ root: classes.tabWH, label: classes.tabItem }}
            />
          </Tabs>
          {tab === 0 ? <Form daemonRunning={this.props.daemonRunning} /> : null}
          {tab === 1 ? this.renderTabs() : null}
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(Configuration);
