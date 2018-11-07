import React from 'react';
import Proptypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Tooltip from '@material-ui/core/Tooltip';
import Icon from '@material-ui/core/Icon';

const styles = {
  ico: {
    position: 'absolute',
    top: '-0.07vh',
    left: 0,
  },
  icoInfo: {
    cursor: 'pointer',
    fontSize: '1.2vw',
    zIndex: 999,
  },
  tooltipText: {
    fontSize: '1vw',
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
          Week - A range of start date (Current date* - 7 days) and end date
          (Current date*)
        </p>
        <p>
          Month - A range of start date (Current date* - 30 days) and end date
          (Current date*)
        </p>
        <p>
          Year - A range of start date (Current date* - 365 days) and end date
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
    const { classes } = this.props;
    return <div className={classes.ico}>{this.renderTooltip()}</div>;
  }
}

export default withStyles(styles)(LegendDate);
