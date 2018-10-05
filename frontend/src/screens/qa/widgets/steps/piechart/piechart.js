import React, { Component } from 'react';
import { VictoryPie, Slice } from 'victory';
import PropTypes from 'prop-types';
import _ from 'lodash';
import flavors from '../../../../../flavors';

const arms = ['b', 'r', 'z'];

export default class PieChart extends Component {
  static propTypes = {
    size: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired,
    arm: PropTypes.number.isRequired,
    renderMetrics: PropTypes.func.isRequired,
    showQaAlarms: PropTypes.func.isRequired,
    hideQaAlarms: PropTypes.func.isRequired,
    qaTests: PropTypes.array,
    monitor: PropTypes.bool,
    flavor: PropTypes.string,
  };

  getColor = test => {
    if (test && !test) return 'gray';
    if (test && test.includes('WARNING') && !test.includes('ALARM'))
      return 'yellow';
    if (
      (test && test.includes('ALARM')) ||
      (!this.props.monitor && test.includes('None') && test.includes('NORMAL'))
    )
      return 'red';
    if (test && test.includes('None')) return 'lightgray';
    if (test && test.includes('Fail')) return 'black';
    return 'green';
  };

  stageColor = index => {
    const currentTest = this.getCurrentTest(index);
    if (currentTest) {
      return this.getColor(currentTest);
    }
    return 'lightgray';
  };

  getCurrentTest = index => {
    const currentCamera = arms[this.props.arm] + index;
    if (this.props.qaTests) {
      const currentTest = this.props.qaTests.find(test => {
        if (Object.keys(test)[0] === currentCamera) return test[currentCamera];
        return null;
      });
      if (flavors[this.props.flavor]) {
        const steps = flavors[this.props.flavor]['step_list'].map(
          flavor => flavor.name
        );
        const step = steps[this.props.step];
        if (currentTest) {
          return currentTest[currentCamera][step];
        }
      }
    }
  };

  renderData = () => {
    return _.map([4, 3, 2, 1, 0, 9, 8, 7, 6, 5], index => {
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
          startAngle={18}
          endAngle={378}
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
                        if (this.getCurrentTest((9 - props.index + 5) % 10)) {
                          this.props.renderMetrics(
                            this.props.step,
                            (9 - props.index + 5) % 10,
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
                        const camera =
                          arms[this.props.arm] + (9 - props.index + 5) % 10;
                        this.props.showQaAlarms(camera, this.props.step);
                        return { style: { fill: 'gray', cursor: 'pointer' } };
                      },
                    },
                    {
                      target: 'labels',
                      mutation: () => {
                        return { style: { display: 'none' } };
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
            labels: { fill: 'black', fontSize: this.props.size / 10 },
          }}
        />
      </svg>
    );
  }
}
