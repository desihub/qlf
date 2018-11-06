import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    flex: 1,
    display: 'flex',
  },
  cardsItens: {
    minHeight: '4.5vh',
    flex: 1,
    margin: '1.5vh 1vw 1vh 1vw',
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
            <CardContent>{`Status: ${this.props.pipelineRunning}`}</CardContent>
          </Card>
        ) : null}
        <Card className={classes.cardsItens}>
          <CardContent>{`Flavor: ${this.props.flavor}`}</CardContent>
        </Card>
        {processId ? (
          <Card className={classes.cardsItens}>
            <CardContent>{`Process Id: ${processId}`}</CardContent>
          </Card>
        ) : null}
        <Card className={classes.cardsItens}>
          <CardContent>{`Exposure: ${this.props.exposureId}`}</CardContent>
        </Card>
        <Card className={classes.cardsItens}>
          <CardContent>{`MJD: ${mjd}`}</CardContent>
        </Card>
        <Card className={classes.cardsItens}>
          <CardContent>{`Date: ${this.formatDate()}`}</CardContent>
        </Card>
      </div>
    );
  }
}

export default withStyles(styles)(Status);
