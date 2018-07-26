import React from 'react';
import Form from './widgets/form/form';
import Display from './widgets/display/display';
import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import PropTypes from 'prop-types';

const styles = {
  container: {
    margin: '1em',
    overflow: 'auto',
    height: '85vh',
    width: 'calc(100vw - 2em)',
  },
};

export default class Configuration extends React.Component {
  static propTypes = {
    daemonRunning: PropTypes.bool.isRequired,
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
        >
          <Tab label="Dark" value={0} />
          <Tab label="Bright" value={1} />
          <Tab label="Gray" value={2} />
        </Tabs>
        {qlScienceTab === 0 ? <Display config={'darksurvey'} /> : null}
        {qlScienceTab === 1 ? <Display config={'brightsurvey'} /> : null}
        {qlScienceTab === 2 ? <Display config={'graysurvey'} /> : null}
      </div>
    );
  };

  renderCalibration = () => {
    const { qlCalibrationTab, qlTab } = this.state;
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
        >
          <Tab label="Flat" value={0} />
          <Tab label="Dark Current" value={1} />
          <Tab label="Bias" value={2} />
          <Tab label="ARC" value={3} />
        </Tabs>
        {qlCalibrationTab === 0 ? <Display config={'flat'} /> : null}
        {qlCalibrationTab === 1 ? <Display config={'darkcurrent'} /> : null}
        {qlCalibrationTab === 2 ? <Display config={'bias'} /> : null}
        {qlCalibrationTab === 3 ? <Display config={'arcs'} /> : null}
      </div>
    );
  };

  renderTabs = () => {
    const { qlTab } = this.state;
    return (
      <div>
        <Tabs
          value={qlTab}
          onChange={this.handleQlTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
          centered
        >
          <Tab label="SCIENCE" value={0} />
          <Tab label="Calibration" value={1} />
        </Tabs>
        {qlTab === 0 ? this.renderScience() : null}
        {qlTab === 1 ? this.renderCalibration() : null}
      </div>
    );
  };

  render() {
    const { tab } = this.state;
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
          >
            <Tab label="QLF" value={0} />
            <Tab label="QL" value={1} />
          </Tabs>
          {tab === 0 ? <Form daemonRunning={this.props.daemonRunning} /> : null}
          {tab === 1 ? this.renderTabs() : null}
        </Paper>
      </div>
    );
  }
}
