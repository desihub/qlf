import React, { Component } from 'react';
import { Card, CardTitle } from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import PropTypes from 'prop-types';

const styles = {
  card: {
    borderLeft: 'solid 4px teal',
    flex: 1,
  },
  select: {
    flex: 1,
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingBottom: '10px',
  },
  button: {
    flex: 1,
    minWidth: '10px',
  },
  value: {
    flex: 1,
    fontSize: 'calc(1vw + 1vh)',
    textAlign: 'center',
  },
  titleContainer: {
    padding: '0px',
    paddingLeft: '10px',
  },
  title: {
    fontSize: 'calc(5px + 1vh)',
    color: 'rgba(0, 0, 0, 0.54)',
  },
};

export default class Control extends Component {
  static propTypes = {
    value: PropTypes.any.isRequired,
    title: PropTypes.string.isRequired,
    change: PropTypes.func.isRequired,
  };

  render() {
    return (
      <Card style={styles.card}>
        <CardTitle
          titleStyle={styles.title}
          style={styles.titleContainer}
          title={this.props.title}
        />
        <div style={styles.select}>
          <FlatButton
            style={styles.button}
            label="<"
            primary={true}
            onClick={() => this.props.change('prev')}
          />
          <span style={styles.value}>{this.props.value}</span>
          <FlatButton
            style={styles.button}
            label=">"
            primary={true}
            onClick={() => this.props.change('next')}
          />
        </div>
      </Card>
    );
  }
}
