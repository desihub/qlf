import React from 'react';
import Modal from '@material-ui/core/Modal';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Petals from '../../../../components/petals/petals';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';
import { FadeLoader } from 'halogenium';
import Button from '@material-ui/core/Button';

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
  controls: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    width: '80%',
    minWidth: 400,
    justifyContent: 'space-evenly',
  },
  radioGroup: {
    display: 'flex',
    flexDirection: 'row',
  },
  button: {
    float: 'right',
  },
};

class ImageModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      arm: null,
      spectrograph: null,
      loading: false,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    handleClose: PropTypes.func.isRequired,
  };

  renderImage = () => {
    const { classes } = this.props;
    if (this.state.arm !== null && this.state.spectrograph !== null)
      return (
        <iframe
          title="image-modal"
          className={classes.iframe}
          frameBorder="0"
          src={`http://localhost:8001/dashboard/fits_to_png/?process_id=1&cam=${
            this.state.arm
          }${this.state.spectrograph}`}
          onLoad={this.loadEnd}
        />
      );
  };

  handleChangeSpectrograph = spectrograph => {
    this.setState({ spectrograph });
    if (this.state.arm !== null) this.loadStart();
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value });
    if (this.state.spectrograph !== null) this.loadStart();
  };

  loadStart = () => {
    this.setState({ loading: true });
  };

  loadEnd = () => {
    this.setState({ loading: false });
  };

  renderLoading = () => {
    if (!this.state.loading) return null;
    return (
      <div style={{ ...styles.loading }}>
        <FadeLoader color="#424242" size="16px" margin="4px" />
      </div>
    );
  };

  clearSelection = () => {
    this.setState({ spectrograph: null, arm: null, loading: false });
  };

  render() {
    const { classes } = this.props;
    return (
      <Modal className={classes.modal} open={true} onClose={this.handleClose}>
        <div className={classes.modalBody}>
          <div className={classes.controls}>
            <div>
              <FormLabel component="legend">Spectrograph:</FormLabel>
              <Petals
                selected={this.state.spectrograph}
                onClick={this.handleChangeSpectrograph}
                size={100}
              />
            </div>
            <div>
              <FormLabel component="legend">Arm:</FormLabel>
              <RadioGroup
                className={classes.radioGroup}
                value={this.state.arm}
                onChange={this.handleChangeArm}
              >
                <FormControlLabel value="b" control={<Radio />} label="b" />
                <FormControlLabel value="r" control={<Radio />} label="r" />
                <FormControlLabel value="z" control={<Radio />} label="z" />
              </RadioGroup>
              <Button
                onClick={this.props.handleClose}
                variant="contained"
                size="small"
                className={classes.button}
              >
                Back
              </Button>
              <Button
                onClick={this.clearSelection}
                variant="contained"
                size="small"
                className={classes.button}
              >
                Clear
              </Button>
            </div>
          </div>
          {this.renderLoading()}
          {this.renderImage()}
        </div>
      </Modal>
    );
  }
}

export default withStyles(styles)(ImageModal);
