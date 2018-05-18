import React from 'react';
import QLFApi from '../../../../containers/offline/connection/qlf-api';
import TextField from '@material-ui/core/TextField';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import _ from 'lodash';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';

const styles = {
  container: {
    margin: '1em',
  },
  label: {
    fontSize: '0.75rem',
    marginTop: '16px',
  },
  title: {
    marginTop: '16px',
    textAlign: 'center',
  },
  button: {
    margin: '1em',
  },
};

export default class Form extends React.Component {
  componentDidMount() {
    this.getCurrentConfiguration();
  }

  state = {
    night: '',
    arms: [],
    input: '',
    output: '',
    exposures: '',
    logfile: '',
    logpipeline: '',
    loglevel: '',
    qlconfig: '',
    spectrographs: [],
    loading: false,
  };

  updateNight = night => {
    this.setState({ night });
  };

  updateExposures = exposures => {
    this.setState({ exposures });
  };

  updateArm = arm => {
    if (this.state.arms.includes(arm)) {
      this.setState({ arms: this.state.arms.filter(a => a !== arm) });
    } else {
      this.setState({ arms: this.state.arms.concat(arm) });
    }
  };

  updateSpectrograph = spectrograph => {
    if (this.state.spectrographs.includes(spectrograph)) {
      this.setState({
        spectrographs: this.state.spectrographs.filter(a => a !== spectrograph),
      });
    } else {
      this.setState({
        spectrographs: this.state.spectrographs.concat(spectrograph),
      });
    }
  };

  updateInput = input => {
    this.setState({ input });
  };

  updateOutput = output => {
    this.setState({ output });
  };

  updateLoglevel = loglevel => {
    this.setState({ loglevel });
  };

  updateLogfile = logfile => {
    this.setState({ logfile });
  };

  updateLogpipeline = logpipeline => {
    this.setState({ logpipeline });
  };

  updateQlconfig = qlconfig => {
    this.setState({ qlconfig });
  };

  updateConfiguration = configuration => {
    if (configuration && configuration.results) {
      const {
        night,
        arms,
        desi_spectro_data,
        desi_spectro_redux,
        exposures,
        logfile,
        logpipeline,
        loglevel,
        qlconfig,
        spectrographs,
      } = configuration.results;
      this.setState({
        night: night,
        arms: arms.split(','),
        input: desi_spectro_data,
        output: desi_spectro_redux,
        exposures: exposures,
        logfile: logfile,
        logpipeline: logpipeline,
        loglevel: loglevel,
        qlconfig: qlconfig,
        spectrographs: spectrographs.split(','),
      });
    }
  };

  getCurrentConfiguration = async () => {
    this.setState({ loading: true });
    const configuration = await QLFApi.getCurrentConfiguration();
    this.setState({ loading: false });
    this.updateConfiguration(configuration);
  };

  getDefaultConfiguration = async () => {
    this.setState({ loading: true });
    const configuration = await QLFApi.getDefaultConfiguration();
    this.setState({ loading: false });
    this.updateConfiguration(configuration);
  };

  render() {
    return (
      <div style={styles.container}>
        {this.state.loading ? <CircularProgress size={50} /> : null}
        <Typography style={styles.title} variant="headline" component="h2">
          Data
        </Typography>
        <TextField
          id="full-width"
          label="Night"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Which night to process? we do not support a list of nights yet."
          fullWidth
          margin="normal"
          value={this.state.night}
          onChange={evt => this.updateNight(evt.value)}
        />
        <TextField
          id="full-width"
          label="Exposures"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Exposure ids to be processed"
          fullWidth
          margin="normal"
          value={this.state.exposures}
          onChange={evt => this.updateExposures(evt.value)}
        />
        <FormControl component="fieldset">
          <FormLabel style={styles.label}>Arms to process</FormLabel>
          <FormGroup row>
            {['b', 'r', 'z'].map(arm => (
              <FormControlLabel
                key={arm}
                control={
                  <Checkbox
                    checked={this.state.arms.includes(arm)}
                    onChange={() => this.updateArm(arm)}
                    value={arm}
                  />
                }
                label={arm}
              />
            ))}
          </FormGroup>
        </FormControl>
        <Divider />
        <FormControl component="fieldset">
          <FormLabel style={styles.label}>Spectrographs to process</FormLabel>
          <FormGroup row>
            {_.range(0, 10).map(id => {
              const spectrograph = id.toString();
              return (
                <FormControlLabel
                  key={id}
                  control={
                    <Checkbox
                      checked={this.state.spectrographs.includes(spectrograph)}
                      onChange={() => this.updateSpectrograph(spectrograph)}
                      value={spectrograph}
                    />
                  }
                  label={id}
                />
              );
            })}
          </FormGroup>
        </FormControl>
        <Divider />
        <Typography style={styles.title} variant="headline" component="h2">
          Input/Output
        </Typography>
        <TextField
          id="full-width"
          label="Input Directory"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Input data directory, e.g. full/path/to/spectro/data"
          fullWidth
          margin="normal"
          value={this.state.input}
          onChange={evt => this.updateInput(evt.value)}
        />
        <TextField
          id="full-width"
          label="Output Directory"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Processing output, e.g. full/path/to/spectro/redux or some other local (fast) scratch area"
          fullWidth
          margin="normal"
          value={this.state.output}
          onChange={evt => this.updateOutput(evt.value)}
        />
        <Divider />
        <Typography style={styles.title} variant="headline" component="h2">
          Log
        </Typography>
        <TextField
          id="full-width"
          label="Log Level"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Log level, e.g. DEBUG, INFO, WARNING or ERROR"
          fullWidth
          margin="normal"
          value={this.state.loglevel}
          onChange={evt => this.updateLoglevel(evt.value)}
        />
        <TextField
          id="full-width"
          label="Log File"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Log file name, e.g. full/path/to/qlf.log this is the main place for following the progress of the data reduction"
          fullWidth
          margin="normal"
          value={this.state.logfile}
          onChange={evt => this.updateLogfile(evt.value)}
        />
        <TextField
          id="full-width"
          label="Log Pipeline"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Log Pipeline name, e.g. full/path/to/pipeline.log this is the main place for following ICS"
          fullWidth
          margin="normal"
          value={this.state.logpipeline}
          onChange={evt => this.updateLogpipeline(evt.value)}
        />
        <TextField
          id="full-width"
          label="Configuration file for the quick look pipeline"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="e.g. full/path/to/desispec/py/desispec/data/quicklook/qlconfig_darksurvey.yaml"
          fullWidth
          margin="normal"
          value={this.state.qlconfig}
          onChange={evt => this.updateQlconfig(evt.value)}
        />
        <Button
          disabled={true}
          variant="raised"
          color="default"
          style={styles.button}
        >
          Save
        </Button>
        <Button
          onClick={this.getDefaultConfiguration}
          variant="raised"
          color="default"
          style={styles.button}
        >
          Default
        </Button>
      </div>
    );
  }
}
