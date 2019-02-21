import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

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
    background: 'white',
    border: '0',
    boxShadow: 'none',
  },
  value: {
    fontSize: '1.2vw',
    textAlign: 'center',
    padding: '5px',
  },
  title: {
    paddingLeft: '10px',
    fontSize: '1.2vw',
    color: 'rgba(0, 0, 0, 0.54)',
    gridArea: 'title',
  },
  text: {
    fontSize: '1.2vw',
  },
};

class Control extends Component {
  static propTypes = {
    value: PropTypes.any.isRequired,
    title: PropTypes.string.isRequired,
    change: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  };

  render() {
    const { classes } = this.props;
    return (
      <Card style={styles.card}>
        <div style={styles.grid}>
          <Typography variant="body2" style={styles.title}>
            {this.props.title}
          </Typography>
          <Button
            style={styles.button}
            onClick={() => this.props.change('prev')}
            classes={{ contained: classes.text }}
            variant="contained"
          >
            &lt;
          </Button>
          <span style={styles.value}>{this.props.value}</span>
          <Button
            style={styles.button}
            onClick={() => this.props.change('next')}
            classes={{ contained: classes.text }}
            variant="contained"
          >
            &gt;
          </Button>
        </div>
      </Card>
    );
  }
}

export default withStyles(styles)(Control);
