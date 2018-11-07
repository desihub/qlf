import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    flex: 1,
    display: 'flex',
  },
  cardsItens: {
    flex: 1,
    padding: 5,
    margin: '1vh 1vw 1vh 1vw',
    borderLeft: 'solid 4px #424242',
    overflow: 'hidden',
    boxShadow:
      '0px 1px 5px 0px rgba(0, 0, 0, 0.2), 0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 3px 1px -2px rgba(0, 0, 0, 0.12)',
    borderRadius: '2px',
    backgroundColor: '#fff',
    fontSize: '1.2vw',
  },
};

class Status extends Component {
  static propTypes = {
    pipelineRunning: PropTypes.string,
    exposureId: PropTypes.string.isRequired,
    mjd: PropTypes.string,
    date: PropTypes.string,
    flavor: PropTypes.string,
    processId: PropTypes.string,
    classes: PropTypes.object.isRequired,
  };

  formatDate = () => {
    if (!this.props.date) return '';
    return this.props.date.replace(/-/g, '');
  };

  render() {
    const { classes } = this.props;
    const mjd = parseFloat(this.props.mjd)
      ? parseFloat(this.props.mjd).toFixed(3)
      : '';
    const processId =
      this.props.processId && !this.props.processId.includes('-')
        ? this.props.processId
        : '';
    return (
      <div style={{ ...styles.container }}>
        {this.props.pipelineRunning ? (
          <Card className={classes.cardsItens}>
            {`Status: ${this.props.pipelineRunning}`}
          </Card>
        ) : null}
        <Card className={classes.cardsItens}>
          {`Flavor: ${this.props.flavor}`}
        </Card>
        {processId ? (
          <Card className={classes.cardsItens}>
            {`Process Id: ${processId}`}
          </Card>
        ) : null}
        <Card className={classes.cardsItens}>
          {`Exposure: ${this.props.exposureId}`}
        </Card>
        <Card className={classes.cardsItens}>{`MJD: ${mjd}`}</Card>
        <Card className={classes.cardsItens}>
          {`Date: ${this.formatDate()}`}
        </Card>
      </div>
    );
  }
}

export default withStyles(styles)(Status);
