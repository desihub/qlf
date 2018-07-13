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

const stepsQa = {
  preproc: ['countpix', 'getbias', 'getrms', 'xwsigma'],
  extract: ['countbins'],
  fiberfl: ['skycont', 'skypeak'],
  skysubs: ['integ', 'skyresid', 'snr'],
};

export default class MetricSelect extends Component {
  static propTypes = {
    step: PropTypes.string.isRequired,
    selectedQA: PropTypes.string,
    camera: PropTypes.string.isRequired,
    selectQA: PropTypes.func.isRequired,
    back: PropTypes.func.isRequired,
    qaTests: PropTypes.array.isRequired,
  };

  renderButtons = step => {
    if (!this.props.qaTests) return null;
    const tests = this.props.qaTests.find(test => {
      if (Object.keys(test)[0] === this.props.camera)
        return test[this.props.camera];
      return null;
    });
    let buttonsStatus = [];
    if (
      tests &&
      tests[this.props.camera] &&
      tests[this.props.camera][step] &&
      tests[this.props.camera][step].steps_status
    ) {
      buttonsStatus = tests[this.props.camera][step].steps_status.map(
        status => {
          return status;
        }
      );
    } else {
      buttonsStatus = undefined;
    }

    return stepsQa[step].map((qa, index) => {
      const selected =
        this.props.selectedQA && this.props.selectedQA.includes(qa)
          ? styles.selected
          : null;
      if (buttonsStatus) {
        const labelColor =
          buttonsStatus[index] === 'NORMAL'
            ? styles.normal
            : buttonsStatus[index] === 'WARNING'
              ? styles.warning
              : styles.failure;
        const label = qa
          .toUpperCase()
          .concat(buttonsStatus[index] !== 'ALARM' ? ' ✓' : ' ✖︎');
        return (
          <FlatButton
            key={index}
            labelStyle={{ ...selected, ...styles.metricLabel }}
            onClick={() => this.props.selectQA('qa' + qa)}
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
            onClick={() => this.props.selectQA('qa' + qa)}
            fullWidth
            style={styles.failure}
            label={qa.toUpperCase() + ' ✖︎'}
            disabled={true}
          />
        );
      }
    });
  };

  renderMetricOptions = () => {
    switch (this.props.step) {
      case 'Pre Processing':
        return (
          <div style={styles.buttons}>{this.renderButtons('preproc')}</div>
        );
      case 'Spectral Extraction':
        return (
          <div style={styles.buttons}>{this.renderButtons('extract')}</div>
        );
      case 'Fiber Flattening':
        return (
          <div style={styles.buttons}>{this.renderButtons('fiberfl')}</div>
        );
      case 'Sky Subtraction':
        return (
          <div style={styles.buttons}>{this.renderButtons('skysubs')}</div>
        );
      default:
        return null;
    }
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
