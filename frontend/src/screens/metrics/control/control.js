import React, { Component } from 'react';
import FlatButton from 'material-ui/FlatButton';
import Card from '@material-ui/core/Card';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';

const styles = {
  card: {
    borderLeft: 'solid 4px #424242',
    marginLeft: '1vw',
    alignSelf: 'center',
  },
  grid: {
    display: 'grid',
    gridTemplateAreas: "'title control control control'",
    alignItems: 'center',
  },
  select: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingBottom: '10px',
  },
  button: {
    minWidth: '10px',
  },
  value: {
    fontSize: '14px',
    textAlign: 'center',
    padding: '5px',
  },
  title: {
    paddingLeft: '10px',
    fontSize: '14px',
    color: 'rgba(0, 0, 0, 0.54)',
    gridArea: 'title',
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
        <div style={styles.grid}>
          <Typography variant="body2" style={styles.title}>
            {this.props.title}
          </Typography>
          <FlatButton
            style={styles.button}
            className="control"
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
