import React from 'react';
import { Card, CardTitle } from 'material-ui/Card';
import PropTypes from 'prop-types';

const styles = {
  card: {
    borderLeft: 'solid 4px teal',
    flex: 1,
    margin: '1.5vh 1vw 1vh 1vw',
  },
  titleStyle: {
    fontSize: '13px',
    color: 'rgba(0, 0, 0, 0.6)',
    lineHeight: '3vh',
  },
  subtitleStyle: {
    fontSize: '13px',
    float: 'right',
    paddingBottom: '8px',
    paddingRight: '8px',
    color: 'rgba(0, 0, 0, 0.80)',
  },
  cardStyle: {
    padding: '0px 0px 0px 8px',
  },
};

export default class Cards extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    subtitle: PropTypes.string.isRequired,
  };

  render() {
    return (
      <Card style={styles.card}>
        <CardTitle
          style={styles.cardStyle}
          titleStyle={styles.titleStyle}
          subtitleStyle={styles.subtitleStyle}
          title={this.props.title}
          subtitle={this.props.subtitle}
        />
      </Card>
    );
  }
}
