import React, { Component } from 'react';
import { VictoryPie, Slice } from 'victory';
import PropTypes from 'prop-types';
import _ from 'lodash';

const arms = ['b', 'r', 'z'];
const steps = ['preproc', 'extract', 'fiberfl', 'skysubs'];

export default class PieChart extends Component {
  static propTypes = {
    size: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired,
    arm: PropTypes.number.isRequired,
    renderMetrics: PropTypes.func.isRequired,
    showQaAlarms: PropTypes.func.isRequired,
    hideQaAlarms: PropTypes.func.isRequired,
    qaTests: PropTypes.array,
  };

  getColor = test => {
    if (test && !test.steps_status) return 'gray';
    if (
      (test && test.steps_status && test.steps_status.includes('FAILURE')) ||
      (test.steps_status.includes('None') &&
        test.steps_status.includes('NORMAL'))
    )
      return 'red';
    if (test && test.steps_status && test.steps_status.includes('None'))
      return 'gray';
    return 'green';
  };

  stageColor = index => {
    const currentTest = this.getCurrentTest(index);
    if (currentTest) {
      return this.getColor(currentTest);
    }
    return 'gray';
  };

  getCurrentTest = index => {
    const currentCamera = arms[this.props.arm] + index;
    if (this.props.qaTests) {
      const currentTest = this.props.qaTests.find(test => {
        if (Object.keys(test)[0] === currentCamera) return test[currentCamera];
        return null;
      });
      const step = steps[this.props.step];
      if (currentTest) {
        return currentTest[currentCamera][step];
      }
    }
  };

  renderData = () => {
    return _.map(_.range(10), index => {
      return {
        x: index,
        y: 1,
        fill: this.stageColor(index),
      };
    });
  };

  render() {
    const data = this.renderData();
    const tooltip = {
      'data-tip': true,
      'data-for': 'tooltip',
    };

    return (
      <svg width={this.props.size} height={this.props.size}>
        <VictoryPie
          padding={0}
          width={this.props.size}
          height={this.props.size}
          standalone={false}
          colorScale={['gray']}
          labelRadius={this.props.size / 3}
          data={data}
          dataComponent={<Slice events={tooltip} />}
          events={[
            {
              target: 'data',
              eventHandlers: {
                onClick: () => {
                  return [
                    {
                      mutation: props => {
                        if (this.getCurrentTest(props.index)) {
                          this.props.renderMetrics(
                            this.props.step,
                            props.index,
                            this.props.arm
                          );
                        }
                        return props;
                      },
                    },
                  ];
                },
                onMouseOver: () => {
                  return [
                    {
                      target: 'data',
                      mutation: props => {
                        const camera = arms[this.props.arm] + props.index;
                        this.props.showQaAlarms(camera, this.props.step);
                        return { style: { fill: 'gray' } };
                      },
                    },
                    {
                      target: 'labels',
                      mutation: () => {
                        return { style: { fill: 'gray' } };
                      },
                    },
                  ];
                },
                onMouseOut: () => {
                  return [
                    {
                      target: 'data',
                      mutation: () => {
                        this.props.hideQaAlarms();
                        return null;
                      },
                    },
                    {
                      target: 'labels',
                      mutation: () => {
                        return null;
                      },
                    },
                  ];
                },
              },
            },
          ]}
          style={{
            data: {
              fillOpacity: 0.9,
              stroke: '#fff',
              strokeWidth: 1,
            },
            labels: { fill: 'white', fontSize: this.props.size / 10 },
          }}
        />
      </svg>
    );
  }
}
