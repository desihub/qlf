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

const apiUrl = process.env.REACT_APP_API;

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
    height: '70vh',
    width: '70vw',
  },
  controlsContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    height: '100%',
    minWidth: 200,
    justifyContent: 'space-evenly',
    borderRight: '1px solid darkgrey',
  },
  column: {
    display: 'flex',
    flexDirection: 'column',
  },
  row: {
    display: 'flex',
    flexDirection: 'row',
  },
  preview: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  loading: {
    position: 'relative',
    top: 200,
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
      processing: null,
      loading: false,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    handleClose: PropTypes.func.isRequired,
    exposure: PropTypes.string.isRequired,
    night: PropTypes.string.isRequired,
  };

  renderImage = () => {
    const { classes } = this.props;
    let url = '';
    if (
      this.state.arm !== null &&
      this.state.processing !== null &&
      this.state.spectrograph !== null
    )
      url = `${apiUrl}dashboard/fits_to_png/?process_id=1&cam=${
        this.state.arm
      }${this.state.spectrograph}&night=${this.props.night}&exposure=${
        this.props.exposure
      }&processing=${this.state.processing}`;
    return (
      <iframe
        title="image-modal"
        className={classes.iframe}
        frameBorder="0"
        src={url}
        onLoad={this.loadEnd}
      />
    );
  };

  handleChangeSpectrograph = spectrograph => {
    this.setState({ spectrograph });
    if (this.state.arm !== null && this.state.processing !== null)
      this.loadStart();
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value });
    if (this.state.spectrograph !== null && this.state.processing !== null)
      this.loadStart();
  };

  handleChangeProcessing = evt => {
    this.setState({ processing: evt.target.value });
    if (this.state.spectrograph !== null && this.state.arm !== null)
      this.loadStart();
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
      <div className={this.props.classes.loading}>
        <FadeLoader color="#424242" size="16px" margin="4px" />
      </div>
    );
  };

  clearSelection = () => {
    this.setState({
      processing: null,
      spectrograph: null,
      arm: null,
      loading: false,
    });
  };

  renderControls = () => {
    const { classes } = this.props;
    return (
      <div className={classes.controlsContainer}>
        <div>
          <FormLabel component="legend">Spectrograph:</FormLabel>
          <Petals
            selected={this.state.spectrograph}
            onClick={this.handleChangeSpectrograph}
            size={100}
          />
        </div>
        <div className={classes.row}>
          <div>
            <FormLabel component="legend">Arm:</FormLabel>
            <div className={classes.row}>
              <RadioGroup
                className={classes.column}
                value={this.state.arm}
                onChange={this.handleChangeArm}
              >
                <FormControlLabel value="b" control={<Radio />} label="b" />
                <FormControlLabel value="r" control={<Radio />} label="r" />
                <FormControlLabel value="z" control={<Radio />} label="z" />
              </RadioGroup>
            </div>
          </div>
          <div>
            <FormLabel component="legend">Processing:</FormLabel>
            <div className={classes.row}>
              <RadioGroup
                className={classes.column}
                value={this.state.processing}
                onChange={this.handleChangeProcessing}
              >
                <FormControlLabel value="raw" control={<Radio />} label="raw" />
                <FormControlLabel
                  value="reduced"
                  control={<Radio />}
                  label="reduced"
                />
              </RadioGroup>
            </div>
          </div>
        </div>
        {this.renderClear()}
      </div>
    );
  };

  renderClose = () => (
    <Button
      onClick={this.props.handleClose}
      variant="raised"
      size="small"
      className={this.props.classes.button}
    >
      Close
    </Button>
  );

  renderClear = () => (
    <Button
      onClick={this.clearSelection}
      variant="raised"
      size="small"
      className={this.props.classes.button}
    >
      Clear
    </Button>
  );

  render() {
    const { classes } = this.props;
    return (
      <Modal className={classes.modal} open={true} onClose={this.handleClose}>
        <div className={classes.modalBody}>
          <div className={classes.row}>
            <div>{this.renderControls()}</div>
            <div className={classes.preview}>
              <FormLabel component="legend">Preview:</FormLabel>
              {this.renderLoading()}
              {this.renderImage()}
              {this.renderClose()}
            </div>
          </div>
        </div>
      </Modal>
    );
  }
}

export default withStyles(styles)(ImageModal);
