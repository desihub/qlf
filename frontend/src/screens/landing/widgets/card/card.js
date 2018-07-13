import React from 'react';
import { Card, CardTitle, CardMedia, CardText } from 'material-ui/Card';
import PropTypes from 'prop-types';
import {
  History,
  RemoveRedEye,
  Web,
  Cloud,
  TrendingUp,
  Assignment,
  ViewModule,
  BrightnessMedium,
  AddToQueue,
} from 'material-ui-icons';

const styles = {
  card: {
    borderLeft: 'solid 4px #424242',
    flex: '1',
    marginRight: '1vw',
    marginBottom: '1vw',
    height: '90%',
    cursor: 'pointer',
  },
  icon: {
    height: '5vw',
    width: '4vw',
  },
  cardMedia: {
    display: 'flex',
    flex: '1',
    justifyContent: 'center',
  },
  titleContainer: {
    padding: '1vw',
  },
  title: {
    fontSize: '2vw',
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
    const isMonitor = this.props.title === 'Pipeline Monitor';
    const deactivate =
      isMonitor && process.env.REACT_APP_DEACTIVATE_MONITOR === 'true'
        ? { color: 'gray', fontWeight: 100 }
        : {};
    switch (this.props.icon) {
      case 'Web':
        return <Web style={{ ...styles.icon, ...deactivate }} />;
      case 'RemoveRedEye':
        return <RemoveRedEye style={styles.icon} />;
      case 'History':
        return <History style={styles.icon} />;
      case 'Cloud':
        return <Cloud style={styles.icon} />;
      case 'TrendingUp':
        return <TrendingUp style={styles.icon} />;
      case 'Assignment':
        return <Assignment style={styles.icon} />;
      case 'ViewModule':
        return <ViewModule style={styles.icon} />;
      case 'BrightnessMedium':
        return <BrightnessMedium style={styles.icon} />;
      case 'AddToQueue':
        return <AddToQueue style={styles.icon} />;
      default:
        return;
    }
  };

  render() {
    const isMonitor =
      this.props.title === 'Pipeline Monitor' &&
      process.env.REACT_APP_DEACTIVATE_MONITOR === 'true';
    const deactivate = isMonitor ? { color: 'gray' } : {};
    const deactivateCard =
      isMonitor && process.env.REACT_APP_DEACTIVATE_MONITOR === 'true'
        ? { borderLeft: 'solid 4px gray' }
        : {};
    return (
      <Card style={{ ...styles.card, ...deactivateCard }}>
        <CardTitle
          titleStyle={{ ...styles.title, ...deactivate }}
          style={styles.titleContainer}
          title={this.props.title}
        />
        <CardMedia style={styles.cardMedia}>
          <div>{this.renderIcon()}</div>
        </CardMedia>
        <CardText style={{ ...styles.subtitle, ...deactivate }}>
          {this.props.subtitle}
        </CardText>
      </Card>
    );
  }
}
