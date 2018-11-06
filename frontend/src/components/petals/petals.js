import React, { Component } from 'react';
import { VictoryPie, Slice } from 'victory';
import PropTypes from 'prop-types';
import _ from 'lodash';

export default class Petals extends Component {
  static propTypes = {
    size: PropTypes.number.isRequired,
    selected: PropTypes.array,
    onClick: PropTypes.func.isRequired,
  };

  state = {
    petalSize: 80,
  };

  componentDidMount() {
    this.updatePetalSize();
  }

  componentWillMount() {
    window.addEventListener('resize', this.updatePetalSize);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updatePetalSize);
  }

  updatePetalSize = () => {
    if (window.outerWidth) {
      this.setState({
        petalSize: (window.outerWidth + window.outerHeight) / this.props.size,
      });
    }
  };

  stageColor = index => {
    if (this.props.selected.includes(index)) return 'green';
    return 'lightgray';
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
      <svg width={this.state.petalSize} height={this.state.petalSize}>
        <VictoryPie
          padding={0}
          width={this.state.petalSize}
          height={this.state.petalSize}
          standalone={false}
          colorScale={['gray']}
          labelRadius={this.state.petalSize / 3}
          data={data}
          startAngle={18}
          endAngle={378}
          dataComponent={<Slice events={tooltip} />}
          events={[
            {
              target: 'data',
              eventHandlers: {
                onClick: () => {
                  return [
                    {
                      mutation: props => {
                        this.props.onClick((9 - props.index + 5) % 10);
                        return { style: { fill: 'green', cursor: 'pointer' } };
                      },
                    },
                  ];
                },
                onMouseOver: () => {
                  return [
                    {
                      target: 'data',
                      mutation: props => {
                        const color = this.props.selected.includes(
                          (9 - props.index + 5) % 10
                        )
                          ? 'green'
                          : 'gray';
                        return { style: { fill: color, cursor: 'pointer' } };
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
            labels: {
              fill: 'black',
              fontSize: this.state.petalSize / 10,
            },
          }}
        />
      </svg>
    );
  }
}
