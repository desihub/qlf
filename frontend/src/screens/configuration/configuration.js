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
    overflowY: 'scroll',
    height: '85vh',
  },
};

export default class Configuration extends React.Component {
  static propTypes = {
    daemonRunning: PropTypes.bool.isRequired,
  };

  state = {
    tab: 0,
  };

  componentDidMount() {
    document.title = 'Configuration';
  }

  handleTabChange = (evt, tab) => {
    this.setState({ tab });
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
            <Tab label="SCIENCE" value={1} />
            <Tab label="FLAT" value={2} />
            <Tab label="ARC" value={3} />
          </Tabs>
          {tab === 0 ? <Form daemonRunning={this.props.daemonRunning} /> : null}
          {tab === 1 ? <Display config={'darksurvey'} /> : null}
          {tab === 2 ? <Display config={'flat'} /> : null}
          {tab === 3 ? <Display config={'arcs'} /> : null}
        </Paper>
      </div>
    );
  }
}
