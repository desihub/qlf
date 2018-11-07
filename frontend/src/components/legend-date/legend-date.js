import React from 'react';
import Proptypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Tooltip from '@material-ui/core/Tooltip';
import Icon from '@material-ui/core/Icon';

const styles = {
  icoInfo: {
    position: 'absolute',
    top: 0,
    right: 0,
    cursor: 'pointer',
    fontSize: '1.5vh',
    zIndex: 999,
  },
  tooltipText: {
    fontSize: '1.5vh',
  },
};

class LegendDate extends React.Component {
  static propTypes = {
    classes: Proptypes.object.isRequired,
  };

  renderLegendDate = () => {
    return (
      <div>
        <p>
          All - A range of start and end date related to available exposure day*
        </p>
        <p>Night - Current date* for both start and end date</p>
        <p>
          Week - A range of start date (Current date* - 7days) and end date
          (Current date*)
        </p>
        <p>
          Month - A range of start date (Current date* - 30days) and end date
          (Current date*)
        </p>
        <p>
          Year - A range of start date (Current date* - 365days) and end date
          (Current date*)
        </p>
        <p>*Day and Current date is observation date</p>
      </div>
    );
  };

  renderTooltip = () => {
    const { classes } = this.props;
    return (
      <Tooltip
        classes={{ tooltip: classes.tooltipText }}
        title={this.renderLegendDate()}
        placement="bottom-end"
      >
        <Icon style={styles.icoInfo}>info</Icon>
      </Tooltip>
    );
  };

  render() {
    return <div>{this.renderTooltip()}</div>;
  }
}

export default withStyles(styles)(LegendDate);
