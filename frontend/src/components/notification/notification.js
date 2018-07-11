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
import { connect } from 'react-redux';
import moment from 'moment';
import { clearNotifications } from '../../containers/online/online-store';

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
    maxHeight: 300,
    overflowY: 'scroll',
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
      errors: [],
      warnings: [],
      // errors: [
      //   { msg: 'Error processing exposure 106', time: '12 minutes ago' },
      //   { msg: 'Available Disk Space 8%', time: '1 hour ago' },
      // ],
      // warnings: [{ msg: 'Available Disk Space 20%', time: '20 hours ago' }],
    };
  }

  static propTypes = {
    notifications: PropTypes.array.isRequired,
    clearNotifications: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  };

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
    this.props.clearNotifications();
    this.setState({ anchorEl: null });
  };

  renderNotifications = () => {
    const { classes } = this.props;
    const count = this.props.notifications.length;
    if (!count) return;
    return (
      <div>
        <List style={styles.listStyle}>
          {this.props.notifications.map((notif, id) => {
            const stylePrimary =
              notif.type === 'ALARM' ? classes.alert : classes.warning;
            const date = moment(new Date(notif.date)).fromNow();
            return (
              <div key={id}>
                <ListItem>
                  <ListItemText
                    primary={notif.text}
                    secondary={date}
                    classes={{
                      primary: stylePrimary,
                      secondary: classes.secondary,
                    }}
                  />
                </ListItem>
                <Divider />
              </div>
            );
          })}
        </List>
        <Button onClick={this.clear} className={classes.button}>
          Clear
        </Button>
      </div>
    );
  };

  render() {
    const { classes } = this.props;
    const count = this.props.notifications.length;
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

const NotificationWithStyles = withStyles(styles)(Notification);

export default connect(
  state => ({
    notifications: state.qlfOnline.notifications,
  }),
  dispatch => ({
    clearNotifications: () => dispatch(clearNotifications()),
  })
)(NotificationWithStyles);
