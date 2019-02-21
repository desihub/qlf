import React from 'react';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Petals from '../../components/petals/petals';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';
import { FadeLoader } from 'halogenium';
import Button from '@material-ui/core/Button';
import PNGViewer from './png-viewer/png-viewer';
import LogViewer from './log-viewer/log-viewer';
import GlobalViewer from './global-viewer/global-viewer';
import SpectraViewer from './spectra-viewer/spectra-viewer';

const styles = {
  controlsContainer: {
    display: 'grid',
    alignItems: 'center',
    width: '12vw',
    justifyContent: 'space-evenly',
    borderRight: '1px solid darkgrey',
    overflowY: 'auto',
    paddingRight: '10px',
    boxSizing: 'border-box',
  },
  column: {
    display: 'flex',
    flexDirection: 'column',
  },
  gridRow: {
    display: 'grid',
    gridTemplateColumns: '12vw calc(100vw - 64px - 12vw)',
    width: 'calc(100vw - 64px)',
    height: 'calc(100vh - 135px)',
  },
  viewer: {
    width: 'calc(100vw - 64px - 12vw)',
  },
  fadeLoaderFull: {
    position: 'absolute',
    paddingLeft: 'calc((100vw - 40px) / 2)',
    paddingTop: 'calc(25vh)',
  },
  fadeLoader: {
    position: 'absolute',
    paddingLeft: 'calc((100vw - 300px) / 2)',
    paddingTop: 'calc(25vh)',
  },
  selection: {
    textAlign: 'center',
  },
  buttons: {
    display: 'grid',
    width: '10vw',
  },
  button: {
    float: 'right',
    fontSize: '1.2vw',
    margin: '10px 0',
  },
  buttonGreen: {
    backgroundColor: 'green',
    color: 'white',
  },
  spectrographLabel: {
    paddingBottom: 10,
  },
  main: {
    margin: '16px',
    padding: '16px',
    height: 'calc(100vh - 135px)',
  },
  title: {
    fontSize: '1.2vw',
  },
  text: {
    fontSize: '1.1vw',
    marginLeft: '0.5vw',
  },
  lineH: {
    height: '4.87vh',
    marginLeft: 0,
  },
  wh: {
    width: '1.7vw',
    height: '3.5vh',
  },
};

class SelectionViewer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectArm: '',
      selectProcessing: '',
      selectSpectrograph: [],
      arm: '',
      spectrograph: [],
      processing: '',
      loading: false,
      preview: false,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    spectrograph: PropTypes.bool,
    armAll: PropTypes.bool,
    arm: PropTypes.bool,
    processing: PropTypes.bool,
  };

  handleChangeSpectrograph = spectrograph => {
    this.setState({
      spectrograph: [spectrograph],
      preview: false,
      loading: false,
    });
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value, preview: false, loading: false });
  };

  handleChangeProcessing = evt => {
    this.setState({
      processing: evt.target.value,
      preview: false,
      loading: false,
    });
  };

  loadStart = () => {
    this.setState({ loading: true });
  };

  loadEnd = () => {
    this.setState({ loading: false });
  };

  renderLoading = () => {
    if (!this.state.loading) return null;
    const showControls =
      this.props.arm || this.props.spectrograph || this.props.processing;
    const classLoading = showControls
      ? styles.fadeLoader
      : styles.fadeLoaderFull;
    return (
      <div className={this.props.classes.loading}>
        <FadeLoader
          style={classLoading}
          color="#424242"
          size="16px"
          margin="4px"
        />
      </div>
    );
  };

  handleSubmit = () => {
    this.setState({
      selectProcessing: this.state.processing,
      selectSpectrograph: this.state.spectrograph,
      selectArm: this.state.arm,
      preview: true,
    });
    this.loadStart();
  };

  clearSelection = () => {
    this.setState({
      selectArm: '',
      selectProcessing: '',
      selectSpectrograph: [],
      processing: '',
      spectrograph: [],
      arm: '',
      loading: false,
    });
  };

  renderSpectrographSelection = () => {
    const { classes } = this.props;
    if (this.props.spectrograph)
      return (
        <div>
          <FormLabel
            className={this.props.classes.spectrographLabel}
            component="legend"
            classes={{ root: classes.title }}
          >
            Spectrograph:
          </FormLabel>
          <Petals
            selected={this.state.spectrograph}
            onClick={this.handleChangeSpectrograph}
            size={22}
          />
        </div>
      );
  };

  renderArmSelection = () => {
    const { classes } = this.props;
    if (this.props.arm)
      return (
        <div className={this.props.classes.selection}>
          <FormLabel component="legend" classes={{ root: classes.title }}>
            Arm:
          </FormLabel>
          <div className={this.props.classes.row}>
            <RadioGroup
              className={this.props.classes.column}
              value={this.state.arm}
              onChange={this.handleChangeArm}
            >
              {this.props.armAll ? (
                <FormControlLabel
                  value="all"
                  control={<Radio classes={{ root: classes.wh }} />}
                  label="All"
                  classes={{ label: classes.text, root: classes.lineH }}
                />
              ) : null}
              <FormControlLabel
                value="b"
                control={<Radio classes={{ root: classes.wh }} />}
                label="b"
                classes={{ label: classes.text, root: classes.lineH }}
              />
              <FormControlLabel
                value="r"
                control={<Radio classes={{ root: classes.wh }} />}
                label="r"
                classes={{ label: classes.text, root: classes.lineH }}
              />
              <FormControlLabel
                value="z"
                control={<Radio classes={{ root: classes.wh }} />}
                label="z"
                classes={{ label: classes.text, root: classes.lineH }}
              />
            </RadioGroup>
          </div>
        </div>
      );
  };

  renderProcessingSelection = () => {
    const { classes } = this.props;
    if (this.props.processing)
      return (
        <div className={this.props.classes.selection}>
          <FormLabel component="legend" classes={{ root: classes.title }}>
            Processing:
          </FormLabel>
          <RadioGroup
            value={this.state.processing}
            onChange={this.handleChangeProcessing}
          >
            <FormControlLabel
              value="raw"
              control={<Radio classes={{ root: classes.wh }} />}
              label="raw"
              classes={{ label: classes.text, root: classes.lineH }}
            />
            <FormControlLabel
              value="reduced"
              control={<Radio classes={{ root: classes.wh }} />}
              label="reduced"
              classes={{ label: classes.text, root: classes.lineH }}
            />
          </RadioGroup>
        </div>
      );
  };

  renderControls = () => {
    const { classes } = this.props;
    if (this.props.arm || this.props.spectrograph || this.props.processing)
      return (
        <div className={classes.controlsContainer}>
          {this.renderSpectrographSelection()}
          {this.renderArmSelection()}
          {this.renderProcessingSelection()}
          <div className={classes.buttons}>
            {this.renderSubmit()}
            {this.renderClear()}
          </div>
        </div>
      );
  };

  renderClear = () => (
    <Button
      onClick={this.clearSelection}
      variant="contained"
      size="small"
      className={this.props.classes.button}
    >
      Clear
    </Button>
  );

  renderSubmit = () => (
    <Button
      onClick={this.handleSubmit}
      variant="contained"
      size="small"
      className={this.props.classes.button}
      classes={{ contained: this.props.classes.buttonGreen }}
      disabled={!this.isValid()}
    >
      Submit
    </Button>
  );

  isValid = () => {
    let valid = true;
    if (this.props.arm) {
      valid = this.state.arm !== '';
    }
    if (this.props.spectrograph) {
      valid = valid && this.state.spectrograph.length !== 0;
    }
    if (this.props.processing) {
      valid = valid && this.state.processing !== '';
    }
    return valid;
  };

  renderViewer = () => {
    if (!this.state.preview) return;
    switch (window.location.pathname) {
      case '/ccd-viewer':
        return (
          <PNGViewer
            processing={this.state.selectProcessing}
            arm={this.state.selectArm}
            spectrograph={this.state.selectSpectrograph}
            loadEnd={this.loadEnd}
          />
        );
      case '/log-viewer':
        return (
          <LogViewer
            arm={this.state.selectArm}
            spectrograph={this.state.selectSpectrograph}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
          />
        );
      case '/fiber-viewer':
        return (
          <GlobalViewer
            screen={'globalfiber'}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            arm={this.state.selectArm}
          />
        );
      case '/focus-viewer':
        return (
          <GlobalViewer
            screen={'globalfocus'}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            arm={this.state.selectArm}
          />
        );
      case '/snr-viewer':
        return (
          <GlobalViewer
            screen={'globalsnr'}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            arm={this.state.selectArm}
          />
        );
      case '/spectra-viewer':
        return (
          <SpectraViewer
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            arm={this.state.selectArm}
          />
        );
      default:
        return null;
    }
  };

  render() {
    const { classes } = this.props;
    const showControls =
      this.props.arm || this.props.spectrograph || this.props.processing;
    return (
      <Paper elevation={4} className={classes.main}>
        <div className={showControls ? classes.gridRow : null}>
          {this.renderControls()}
          <div className={showControls ? classes.viewer : null}>
            {this.renderLoading()}
            {this.renderViewer()}
          </div>
        </div>
      </Paper>
    );
  }
}

export default withStyles(styles)(SelectionViewer);
