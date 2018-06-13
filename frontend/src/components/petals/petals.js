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

  stageColor = index => {
    if (this.props.selected.includes(index)) return 'green';
    return 'gray';
  };

  renderData = () => {
    return _.map(_.range(9, -1), index => {
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
                        this.props.onClick(9 - props.index);
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
                          9 - props.index
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
            labels: { fill: 'white', fontSize: this.props.size / 10 },
          }}
        />
      </svg>
    );
  }
}
