import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  title: {
    fontSize: '2.2vh',
  },
  subTitle: {
    fontSize: '1.25vw',
  },
  btn: {
    fontSize: '1.1vw',
  },
};

class ConfirmDialog extends React.Component {
  static propTypes = {
    title: PropTypes.string,
    subtitle: PropTypes.string,
    onConfirm: PropTypes.func.isRequired,
    open: PropTypes.bool.isRequired,
    handleClose: PropTypes.func.isRequired,
    classes: PropTypes.object,
  };

  handleConfirmation = () => {
    this.props.onConfirm();
    this.props.handleClose();
  };

  render() {
    return (
      <div>
        <Dialog
          open={this.props.open}
          onClose={this.handleClose}
          fullWidth={true}
        >
          <DialogTitle
            disableTypography={true}
            classes={{ root: this.props.classes.title }}
          >
            {this.props.title}
          </DialogTitle>
          <DialogContent>
            <DialogContentText classes={{ root: this.props.classes.subTitle }}>
              {this.props.subtitle}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button
              classes={{ label: this.props.classes.btn }}
              onClick={this.props.handleClose}
              color="primary"
            >
              Cancel
            </Button>
            <Button
              classes={{ label: this.props.classes.btn }}
              onClick={this.handleConfirmation}
              color="primary"
              autoFocus
            >
              Yes
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default withStyles(styles)(ConfirmDialog);
