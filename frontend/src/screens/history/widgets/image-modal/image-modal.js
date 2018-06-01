import React from 'react';
import Modal from '@material-ui/core/Modal';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Petals from '../../../../../components/petals/petals';

const styles = {
  modalBody: {
    position: 'absolute',
    backgroundColor: 'white',
    boxShadow: 1,
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  iframe: {
    height: '60vh',
    width: '70vw',
  },
};

class ImageModal extends React.Component {
  static propTypes = {
    classes: PropTypes.object,
  };

  render() {
    const { classes } = this.props;
    return (
      <Modal className={classes.modal} open={true} onClose={this.handleClose}>
        <div className={classes.modalBody}>
          <Petals onClick={() => {}} size={100} />
          <iframe
            className={classes.iframe}
            frameBorder="0"
            src="http://localhost:8001/dashboard/fits_to_png/?process_id=1&cam=b0"
          />
        </div>
      </Modal>
    );
  }
}

export default withStyles(styles)(ImageModal);
