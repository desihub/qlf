import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Popover from '@material-ui/core/Popover';
import QlfApi from '../../../../../containers/offline/connection/qlf-api';

const styles = theme => ({
  typography: {
    margin: theme.spacing.unit * 2,
    cursor: 'pointer',
  },
  text: {
    fontSize: '1.2vw',
  },
});

class CCDSelector extends React.Component {
  static propTypes = {
    anchorEl: PropTypes.object,
    classes: PropTypes.object.isRequired,
    handleClose: PropTypes.func.isRequired,
    openCCDViewer: PropTypes.func.isRequired,
    flavor: PropTypes.string,
    processId: PropTypes.number,
  };

  state = {
    spectra: false,
    ccd: false,
  };

  openViewer = viewer => {
    this.props.handleClose();
    this.props.openCCDViewer(viewer);
  };

  componentWillReceiveProps(nextProps) {
    if (nextProps.anchorEl != null) this.checkFiles();
  }

  checkFiles = async () => {
    const { spectra, ccd } = await QlfApi.checkViewFiles(this.props.processId);
    this.setState({ spectra, ccd });
  };

  render() {
    const { classes, anchorEl } = this.props;

    return (
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
        {this.state.ccd ? (
          <Typography
            className={classes.typography}
            onClick={() => this.openViewer('ccd')}
            classes={{ root: classes.text }}
          >
            CCD
          </Typography>
        ) : null}
        {this.props.flavor === 'science' ? (
          <Typography
            key="fiber"
            className={classes.typography}
            onClick={() => this.openViewer('fiber')}
            classes={{ root: classes.text }}
          >
            Fibers
          </Typography>
        ) : null}
        {this.props.flavor === 'science' && this.state.spectra ? (
          <Typography
            key="spectra"
            className={classes.typography}
            onClick={() => this.openViewer('spectra')}
            classes={{ root: classes.text }}
          >
            Spectra
          </Typography>
        ) : null}
        {/* <Typography
          className={classes.typography}
          onClick={() => this.openViewer('focus')}
        >
          Focus
        </Typography>
        <Typography
          className={classes.typography}
          onClick={() => this.openViewer('snr')}
        >
          SNR
        </Typography> */}
      </Popover>
    );
  }
}

export default withStyles(styles)(CCDSelector);
