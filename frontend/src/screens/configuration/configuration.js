import React from 'react';
import Form from './widgets/form/form';
import Display from './widgets/display/display';
import Paper from 'material-ui-next/Paper';
import Tabs, { Tab } from 'material-ui-next/Tabs';

const styles = {
  container: {
    margin: '1em',
    overflowY: 'scroll',
    height: '85vh',
  },
};

export default class Configuration extends React.Component {
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
            <Tab label="QL" value={1} />
          </Tabs>
          {tab === 0 ? <Form /> : null}
          {tab === 1 ? <Display /> : null}
        </Paper>
      </div>
    );
  }
}
