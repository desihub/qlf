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
import PNGViewer from './png-preview/png-preview';

const styles = {
  controlsContainer: {
    display: 'grid',
    alignItems: 'center',
    minWidth: 200,
    justifyContent: 'space-evenly',
    borderRight: '1px solid darkgrey',
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
  loading: {
    position: 'absolute',
    top: '80px',
    left: '50px',
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
  };

  handleChangeSpectrograph = spectrograph => {
    this.setState({ spectrograph: [spectrograph] });
    if (
      this.state.arm !== null &&
      this.state.processing !== null &&
      spectrograph !== this.state.spectrograph[0]
    )
      this.loadStart();
  };

  handleChangeArm = evt => {
    this.setState({ arm: evt.target.value });
    if (this.state.spectrograph.length !== 0 && this.state.processing !== null)
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
    return (
      <div className={this.props.classes.loading}>
        <FadeLoader color="#424242" size="16px" margin="4px" />
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

  renderSpectrographSelection = () => (
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

  renderArmSelection = () => (
    <div>
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

  renderProcessingSelection = () => (
    <div>
      <FormLabel component="legend">Processing:</FormLabel>
      <RadioGroup
        value={this.state.processing}
        onChange={this.handleChangeProcessing}
      >
        <FormControlLabel value="raw" control={<Radio />} label="raw" />
        <FormControlLabel value="reduced" control={<Radio />} label="reduced" />
      </RadioGroup>
    </div>
  );

  renderControls = () => {
    const { classes } = this.props;
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

  render() {
    const { classes } = this.props;
    return (
      <Paper elevation={4} style={styles.main}>
        <div className={classes.gridRow}>
          {this.renderControls()}
          {this.renderLoading()}
          <PNGViewer
            processing={this.state.processing}
            arm={this.state.arm}
            spectrograph={this.state.spectrograph}
            loadEnd={this.loadEnd}
          />
        </div>
      </Paper>
    );
  }
}

export default withStyles(styles)(SelectionViewer);
