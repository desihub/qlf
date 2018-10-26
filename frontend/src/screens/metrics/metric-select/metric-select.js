import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import FlatButton from 'material-ui/FlatButton';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

const styles = {
  card: {
    borderLeft: 'solid 4px #424242',
    margin: '0.5vh 0.5vw',
  },
  headerMetrics: {
    display: 'grid',
    gridTemplateAreas: "'button button'",
    justifyContent: 'space-between',
    marginLeft: 8,
  },
  titleContainer: {
    padding: '0px',
    paddingLeft: '1vw',
  },
  title: {
    fontSize: '14px',
    color: 'rgba(0, 0, 0, 0.54)',
  },
  buttons: {
    display: 'grid',
    gridTemplateAreas: "'button button' 'button button'",
    justifyContent: 'space-around',
    fontSize: '14px',
  },
  selected: {
    fontWeight: 'bold',
  },
  metricLabel: {
    fontSize: '14px',
  },
  failure: {
    color: 'red',
  },
  normal: {
    color: 'green',
  },
  warning: {
    color: '#EFD469',
  },
  back: {
    color: 'red',
  },
};

export default class MetricSelect extends Component {
  static propTypes = {
    step: PropTypes.string.isRequired,
    selectedQA: PropTypes.string,
    camera: PropTypes.string.isRequired,
    selectQA: PropTypes.func.isRequired,
    back: PropTypes.func.isRequired,
    qaTests: PropTypes.array.isRequired,
    stepsQa: PropTypes.object,
  };

  renderButtons = step => {
    if (!this.props.qaTests) return null;
    const tests = this.props.qaTests.find(test => {
      if (Object.keys(test)[0] === this.props.camera)
        return test[this.props.camera];
      return null;
    });

    let buttonsStatus = [];
    if (tests && tests[this.props.camera] && tests[this.props.camera][step]) {
      buttonsStatus = tests[this.props.camera][step].map(status => {
        return status;
      });
    } else {
      buttonsStatus = undefined;
    }

    if (!this.props.stepsQa[step]) return;
    return this.props.stepsQa[step].map((qa, index) => {
      const qaName = Object.keys(qa)[0];
      const qaDisplay = qa[qaName];
      const selected =
        this.props.selectedQA && this.props.selectedQA.includes(qaName)
          ? styles.selected
          : null;
      if (buttonsStatus && buttonsStatus[index]) {
        const labelColor =
          buttonsStatus[index] === 'NORMAL'
            ? styles.normal
            : buttonsStatus[index] === 'WARNING'
              ? styles.warning
              : styles.failure;
        const label = qaDisplay
          .toUpperCase()
          .concat(
            buttonsStatus[index].toUpperCase() === 'NORMAL' ? ' ✓' : ' ✖︎'
          );
        return (
          <FlatButton
            key={index}
            labelStyle={{ ...selected, ...styles.metricLabel }}
            onClick={() => this.props.selectQA('qa' + qaName)}
            fullWidth
            style={labelColor}
            label={label}
            // primary={buttonsStatus[index]}
            secondary={!buttonsStatus[index]}
          />
        );
      } else {
        return (
          <FlatButton
            key={index}
            labelStyle={{ ...selected, ...styles.metricLabel }}
            onClick={() => this.props.selectQA('qa' + qaName)}
            fullWidth
            style={styles.failure}
            label={qaDisplay.toUpperCase() + ' ✖︎'}
            disabled={true}
          />
        );
      }
    });
  };

  renderMetricOptions = () => {
    return (
      <div style={styles.buttons}>{this.renderButtons(this.props.step)}</div>
    );
  };

  renderTitle = () => {
    return (
      <div style={styles.headerMetrics}>
        <Typography variant="body2" style={styles.title}>
          Metrics
        </Typography>
        <Button style={styles.back} onClick={this.props.back}>
          Back
        </Button>
      </div>
    );
  };

  render() {
    return (
      <Card style={styles.card}>
        {this.renderTitle()}
        {this.renderMetricOptions()}
      </Card>
    );
  }
}
