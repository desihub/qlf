import React from 'react';
import Card from '@material-ui/core/Card';
import Typography from '@material-ui/core/Typography';
import PropTypes from 'prop-types';
import Icon from '@material-ui/core/Icon';

const styles = {
  card: {
    borderLeft: 'solid 4px #424242',
    flex: '1',
    marginRight: '1vw',
    marginBottom: '1vw',
    height: '90%',
    cursor: 'pointer',
    display: 'flex',
    flexDirection: 'column',
  },
  icon: {
    fontSize: '7vw',
  },
  cardMedia: {
    alignItems: 'center',
    justifyContent: 'center',
    display: 'flex',
  },
  title: {
    fontSize: '2vw',
    padding: '1vw',
  },
  subtitle: {
    fontSize: '1.2vw',
    padding: '1vw',
  },
};

export default class Cards extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    subtitle: PropTypes.string.isRequired,
    icon: PropTypes.string.isRequired,
  };

  renderIcon = () => {
    const isOffline =
      this.props.title === 'Pipeline Monitor' ||
      this.props.title === 'Configuration';
    const deactivate =
      isOffline && process.env.REACT_APP_OFFLINE === 'true'
        ? { color: 'gray', fontWeight: 100 }
        : {};
    switch (this.props.icon) {
      case 'Web':
        return <Icon style={{ ...styles.icon, ...deactivate }}>web</Icon>;
      case 'RemoveRedEye':
        return (
          <Icon style={{ ...styles.icon, ...deactivate }}>remove_red_eye</Icon>
        );
      case 'History':
        return <Icon style={{ ...styles.icon, ...deactivate }}>history</Icon>;
      case 'Cloud':
        return <Icon style={{ ...styles.icon, ...deactivate }}>cloud</Icon>;
      case 'TrendingUp':
        return (
          <Icon style={{ ...styles.icon, ...deactivate }}>trending_up</Icon>
        );
      case 'Assignment':
        return (
          <Icon style={{ ...styles.icon, ...deactivate }}>assignment</Icon>
        );
      case 'ViewModule':
        return (
          <Icon style={{ ...styles.icon, ...deactivate }}>view_module</Icon>
        );
      case 'BrightnessMedium':
        return (
          <Icon style={{ ...styles.icon, ...deactivate }}>
            brightness_medium
          </Icon>
        );
      case 'AddToQueue':
        return (
          <Icon style={{ ...styles.icon, ...deactivate }}>add_to_queue</Icon>
        );
      default:
        return;
    }
  };

  render() {
    const isOffline =
      (this.props.title === 'Configuration' ||
        this.props.title === 'Pipeline Monitor') &&
      process.env.REACT_APP_OFFLINE === 'true';
    const deactivate = isOffline ? { color: 'gray' } : {};
    const deactivateCard =
      isOffline && process.env.REACT_APP_OFFLINE === 'true'
        ? { borderLeft: 'solid 4px gray' }
        : {};
    return (
      <Card style={{ ...styles.card, ...deactivateCard }}>
        <Typography style={{ ...styles.title, ...deactivate }}>
          {this.props.title}
        </Typography>
        <div style={styles.cardMedia}>{this.renderIcon()}</div>
        <Typography style={{ ...styles.subtitle, ...deactivate }}>
          {this.props.subtitle}
        </Typography>
      </Card>
    );
  }
}
