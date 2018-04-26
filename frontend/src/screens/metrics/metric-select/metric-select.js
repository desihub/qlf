import React, { Component } from 'react';
import { Card, CardTitle } from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import PropTypes from 'prop-types';

const styles = {
  card: {
    borderLeft: 'solid 4px teal',
    flex: 1,
    margin: '0.5vh 0.5vw',
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
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
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
};

const stepsQa = {
  preproc: ['countpix', 'getbias', 'getrms', 'xwsigma'],
  extract: ['countbins'],
  fiberfl: ['integ', 'skycont', 'skypeak', 'skyresid'],
  skysubs: ['snr'],
};

export default class MetricSelect extends Component {
  static propTypes = {
    step: PropTypes.string.isRequired,
    selectedQA: PropTypes.string,
    camera: PropTypes.string.isRequired,
    selectQA: PropTypes.func.isRequired,
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
          return status === 'NORMAL';
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
        const labelColor = buttonsStatus[index]
          ? styles.normal
          : styles.failure;
        const label = qa
          .toUpperCase()
          .concat(buttonsStatus[index] ? ' ✓' : ' ✖︎');
        return (
          <FlatButton
            key={index}
            labelStyle={{ ...selected, ...styles.metricLabel }}
            onClick={() => this.props.selectQA('qa' + qa)}
            fullWidth
            style={labelColor}
            label={label}
            primary={buttonsStatus[index]}
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

  render() {
    return (
      <Card style={styles.card}>
        <CardTitle
          titleStyle={styles.title}
          style={styles.titleContainer}
          title={'Metrics'}
        />
        {this.renderMetricOptions()}
      </Card>
    );
  }
}
