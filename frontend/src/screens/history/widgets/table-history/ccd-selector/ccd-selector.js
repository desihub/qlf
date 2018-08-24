import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Popover from '@material-ui/core/Popover';

const styles = theme => ({
  typography: {
    margin: theme.spacing.unit * 2,
    cursor: 'pointer',
  },
});

class CCDSelector extends React.Component {
  static propTypes = {
    anchorEl: PropTypes.object,
    classes: PropTypes.object.isRequired,
    handleClose: PropTypes.func.isRequired,
    openCCDViewer: PropTypes.func.isRequired,
  };

  openViewer = viewer => {
    this.props.handleClose();
    this.props.openCCDViewer(viewer);
  };

  render() {
    const { classes, anchorEl } = this.props;

    return (
      <div>
        <Popover
          open={Boolean(anchorEl)}
          anchorEl={anchorEl}
          onClose={this.props.handleClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'center',
          }}
        >
          <Typography
            className={classes.typography}
            onClick={() => this.openViewer('ccd')}
          >
            CCD
          </Typography>
          <Typography
            className={classes.typography}
            onClick={() => this.openViewer('fiber')}
          >
            Fibers
          </Typography>
          <Typography
            className={classes.typography}
            onClick={() => this.openViewer('focus')}
          >
            Focus
          </Typography>
        </Popover>
      </div>
    );
  }
}

export default withStyles(styles)(CCDSelector);
