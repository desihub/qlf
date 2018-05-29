import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Badge from '@material-ui/core/Badge';
import Icon from '@material-ui/core/Icon';
import Popover from '@material-ui/core/Popover';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';

const styles = {
  container: {
    cursor: 'pointer',
  },
  margin: {
    margin: 1,
  },
  padding: {
    padding: 2,
  },
  notificationsIcon: {
    fontSize: 20,
    alignSelf: 'center',
    paddingRight: '8px',
    cursor: 'pointer',
  },
  badge: {
    height: 16,
    width: 16,
    top: -5,
    right: 0,
  },
  alert: {
    color: 'rgb(255, 61, 0)',
  },
  warning: {
    color: '#FF6F00',
  },
  listStyle: {
    padding: 0,
  },
  none: {
    display: 'none',
  },
};

class Notification extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      anchorEl: null,
      errors: [
        { msg: 'Error processing exposure 106', time: '12 minutes ago' },
        { msg: 'Available Disk Space 8%', time: '1 hour ago' },
      ],
      warnings: [{ msg: 'Available Disk Space 20%', time: '20 hours ago' }],
    };
  }

  handleNotificationClick = event => {
    this.setState({
      anchorEl: event.currentTarget,
    });
  };

  handlePopOverClose = () => {
    this.setState({
      anchorEl: null,
    });
  };

  clear = () => {
    this.setState({ warnings: [], errors: [], anchorEl: null });
  };

  renderNotifications = () => {
    const { classes } = this.props;
    const count = this.state.errors.length + this.state.warnings.length;
    if (!count) return;
    return (
      <List style={styles.listStyle}>
        {this.state.errors.map(err => {
          return (
            <div key={err.time}>
              <ListItem>
                <ListItemText
                  primary={err.msg}
                  secondary={err.time}
                  classes={{
                    primary: classes.alert,
                    secondary: classes.secondary,
                  }}
                />
              </ListItem>
              <Divider />
            </div>
          );
        })}
        {this.state.warnings.map(warn => (
          <div key={warn.time}>
            <ListItem key={1}>
              <ListItemText
                primary={warn.msg}
                secondary={warn.time}
                classes={{
                  primary: classes.warning,
                  secondary: classes.secondary,
                }}
              />
            </ListItem>
            <Divider />
          </div>
        ))}
        <Button onClick={this.clear} className={classes.button}>
          Clear
        </Button>
      </List>
    );
  };

  render() {
    const { classes } = this.props;
    const count = this.state.errors.length + this.state.warnings.length;
    const badge = count ? classes.badge : classes.none;
    return (
      <div style={styles.container}>
        <Popover
          open={Boolean(this.state.anchorEl)}
          anchorEl={this.state.anchorEl}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          onClose={this.handlePopOverClose}
          elevation={1}
        >
          {this.renderNotifications()}
        </Popover>
        <Badge
          className={classes.margin}
          badgeContent={count}
          classes={{
            root: classes.root,
            badge: badge,
          }}
          onClick={this.handleNotificationClick}
          color="error"
        >
          <Icon style={styles.notificationsIcon}>notifications</Icon>
        </Badge>
      </div>
    );
  }
}

Notification.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Notification);
