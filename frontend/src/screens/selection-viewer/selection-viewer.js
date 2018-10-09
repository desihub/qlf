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

const styles = {
  controlsContainer: {
    display: 'grid',
    alignItems: 'center',
    width: 200,
    justifyContent: 'space-evenly',
    borderRight: '1px solid darkgrey',
    overflowY: 'auto',
  },
  column: {
    display: 'flex',
    flexDirection: 'column',
  },
  gridRow: {
    display: 'grid',
    gridTemplateColumns: 'auto auto',
    height: 'calc(100vh - 135px)',
  },
  viewer: {
    width: 'calc(100vw - 280px)',
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
  button: {
    float: 'right',
  },
  spectrographLabel: {
    paddingBottom: 10,
  },
  main: {
    margin: '16px',
    padding: '16px',
    height: 'calc(100vh - 135px)',
  },
};

class SelectionViewer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      arm: null,
      spectrograph: [],
      processing: null,
      loading: false,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    spectrograph: PropTypes.bool,
    arm: PropTypes.bool,
    processing: PropTypes.bool,
  };

  handleChangeSpectrograph = spectrograph => {
    this.setState({ spectrograph: [spectrograph] });
    if (
      this.props.processing
        ? this.state.arm !== null &&
          this.state.processing !== null &&
          spectrograph !== this.state.spectrograph[0]
        : this.state.arm !== null && spectrograph !== this.state.spectrograph[0]
    )
      this.loadStart();
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value });
    if (
      this.props.processing
        ? this.state.spectrograph.length !== 0 && this.state.processing !== null
        : this.state.spectrograph.length !== 0
    )
      this.loadStart();
  };

  handleChangeProcessing = evt => {
    this.setState({ processing: evt.target.value });
    if (this.state.spectrograph.length !== 0 && this.state.arm !== null)
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

  clearSelection = () => {
    this.setState({
      processing: null,
      spectrograph: [],
      arm: null,
      loading: false,
    });
  };

  renderSpectrographSelection = () => {
    if (this.props.spectrograph)
      return (
        <div>
          <FormLabel
            className={this.props.classes.spectrographLabel}
            component="legend"
          >
            Spectrograph:
          </FormLabel>
          <Petals
            selected={this.state.spectrograph}
            onClick={this.handleChangeSpectrograph}
            size={100}
          />
        </div>
      );
  };

  renderArmSelection = () => {
    if (this.props.arm)
      return (
        <div className={this.props.classes.selection}>
          <FormLabel component="legend">Arm:</FormLabel>
          <div className={this.props.classes.row}>
            <RadioGroup
              className={this.props.classes.column}
              value={this.state.arm}
              onChange={this.handleChangeArm}
            >
              <FormControlLabel value="b" control={<Radio />} label="b" />
              <FormControlLabel value="r" control={<Radio />} label="r" />
              <FormControlLabel value="z" control={<Radio />} label="z" />
            </RadioGroup>
          </div>
        </div>
      );
  };

  renderProcessingSelection = () => {
    if (this.props.processing)
      return (
        <div className={this.props.classes.selection}>
          <FormLabel component="legend">Processing:</FormLabel>
          <RadioGroup
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
          {this.renderClear()}
        </div>
      );
  };

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

  renderViewer = () => {
    switch (window.location.pathname) {
      case '/ccd-viewer':
        return (
          <PNGViewer
            processing={this.state.processing}
            arm={this.state.arm}
            spectrograph={this.state.spectrograph}
            loadEnd={this.loadEnd}
          />
        );
      case '/log-viewer':
        return (
          <LogViewer
            arm={this.state.arm}
            spectrograph={this.state.spectrograph}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            loading={this.state.loading}
          />
        );
      case '/fiber-viewer':
        return (
          <GlobalViewer
            screen={'globalfiber'}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            arm={this.state.arm}
          />
        );
      case '/focus-viewer':
        return (
          <GlobalViewer
            screen={'globalfocus'}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            arm={this.state.arm}
          />
        );
      case '/snr-viewer':
        return (
          <GlobalViewer
            screen={'globalsnr'}
            loadEnd={this.loadEnd}
            loadStart={this.loadStart}
            arm={this.state.arm}
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
