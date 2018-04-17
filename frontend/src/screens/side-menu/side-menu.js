import React from 'react';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import FlatButton from 'material-ui/FlatButton';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

const styles = {
  linkStyle: { textDecoration: 'none' },
};

export default class Sidemenu extends React.Component {
  static propTypes = {
    openDrawer: PropTypes.bool.isRequired,
    closeDrawer: PropTypes.func.isRequired,
  };

  render() {
    return (
      <div>
        <Drawer open={this.props.openDrawer}>
          <Link
            style={styles.linkStyle}
            onClick={() => this.props.closeDrawer('/')}
            to="/"
          >
            <MenuItem>Home</MenuItem>
          </Link>
          <Link
            style={styles.linkStyle}
            onClick={() => this.props.closeDrawer('/monitor-realtime')}
            to="/monitor-realtime"
          >
            <MenuItem>Pipeline Monitor</MenuItem>
          </Link>
          <Link
            style={styles.linkStyle}
            onClick={() => this.props.closeDrawer('/qa-realtime')}
            to="/qa-realtime"
          >
            <MenuItem>QA</MenuItem>
          </Link>
          <Link
            style={styles.linkStyle}
            onClick={() => this.props.closeDrawer('/processing_history')}
            to="/processing-history"
          >
            <MenuItem>Processing History</MenuItem>
          </Link>
          <FlatButton
            onClick={this.props.closeDrawer}
            label="Close"
            secondary={true}
            fullWidth={true}
          />
        </Drawer>
      </div>
    );
  }
}
