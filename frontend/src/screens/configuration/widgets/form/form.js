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
import Grid from '@material-ui/core/Grid';

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
    qlconfig: '',
    spectrographs: [],
    loading: false,
    minInterval: '',
    maxInterval: '',
    maxExposures: '',
    allowedDelay: '',
    baseExposures: '',
  };

  updateMinInterval = minInterval => {
    this.setState({ minInterval });
  };

  updateMaxInterval = maxInterval => {
    this.setState({ maxInterval });
  };

  updateMaxExposures = maxExposures => {
    this.setState({ maxExposures });
  };

  updateAllowedDelay = allowedDelay => {
    this.setState({ allowedDelay });
  };

  updateBaseExposures = baseExposures => {
    this.setState({ baseExposures });
  };

  updateExposures = exposures => {
    this.setState({ exposures });
  };

  updateArm = arm => {
    if (this.state.arms.includes(arm)) {
      this.setState({
        arms: this.state.arms.filter(a => a !== arm),
        spectrographs: this.state.spectrographs.filter(
          spec => !spec.includes(arm)
        ),
      });
    } else {
      this.setState({
        arms: this.state.arms.concat(arm),
        spectrographs: this.state.spectrographs
          .filter(spec => !spec.includes(arm))
          .concat(_.range(0, 10).map(spec => `${arm}${spec}`)),
      });
    }
  };

  updateSpectrograph = (spectrograph, arm) => {
    if (this.state.spectrographs.includes(`${arm}${spectrograph}`)) {
      this.setState({
        spectrographs: this.state.spectrographs.filter(
          spec => spec !== `${arm}${spectrograph}`
        ),
      });
    } else {
      this.setState({
        spectrographs: this.state.spectrographs.concat(`${arm}${spectrograph}`),
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
        allowed_delay,
        arms,
        desi_spectro_data,
        desi_spectro_redux,
        exposures,
        min_interval,
        max_interval,
        max_exposures,
        qlconfig,
        spectrographs,
        base_exposures_path,
      } = configuration.results;
      let flatSpectrographs = [];
      if (spectrographs && arms)
        flatSpectrographs = _.flatten(
          spectrographs
            .split(',')
            .map(spec => arms.split(',').map(arm => `${arm}${spec}`))
        );
      this.setState({
        arms: arms.split(','),
        input: desi_spectro_data,
        output: desi_spectro_redux,
        exposures: exposures,
        qlconfig: qlconfig,
        spectrographs: flatSpectrographs,
        minInterval: min_interval,
        maxInterval: max_interval,
        maxExposures: max_exposures,
        allowedDelay: allowed_delay,
        baseExposures: base_exposures_path,
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
          Exposure Generator
        </Typography>
        <TextField
          label="Min Interval"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Minimum interval for exposure generation (minutes)"
          fullWidth
          margin="normal"
          value={this.state.minInterval}
          onChange={evt => this.updateMinInterval(evt.value)}
        />
        <TextField
          label="Max Interval"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Maximum interval for exposure generation (minutes)"
          fullWidth
          margin="normal"
          value={this.state.maxInterval}
          onChange={evt => this.updateMaxInterval(evt.value)}
        />
        <TextField
          label="Allowed Delay"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Delay for the next available exposure (seconds)"
          fullWidth
          margin="normal"
          value={this.state.allowedDelay}
          onChange={evt => this.updateAllowedDelay(evt.value)}
        />
        <TextField
          label="Max Exposures"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Maximum number exposures generated per run"
          fullWidth
          margin="normal"
          value={this.state.maxExposures}
          onChange={evt => this.updateMaxExposures(evt.value)}
        />
        <Typography style={styles.title} variant="headline" component="h2">
          Pipeline
        </Typography>
        <FormControl component="fieldset">
          <Grid container spacing={24}>
            <Grid item>
              <FormLabel style={styles.label}>Arms to process</FormLabel>
              <FormGroup column="true">
                {['b', 'r', 'z'].map(arm => (
                  <FormGroup key={arm} row>
                    <FormControlLabel
                      control={
                        <Checkbox
                          checked={this.state.arms.includes(arm)}
                          onChange={() => this.updateArm(arm)}
                          value={arm}
                        />
                      }
                      label={arm}
                    />
                  </FormGroup>
                ))}
              </FormGroup>
            </Grid>
            <Grid item xs>
              <FormLabel style={styles.label}>
                Spectrographs to process
              </FormLabel>
              <FormGroup column="true">
                {['b', 'r', 'z'].map(arm => (
                  <FormGroup key={arm} row>
                    {_.range(0, 10).map(id => {
                      const spectrograph = id.toString();
                      return (
                        <FormControlLabel
                          key={id}
                          control={
                            <Checkbox
                              checked={this.state.spectrographs.includes(
                                `${arm}${spectrograph}`
                              )}
                              onChange={() =>
                                this.updateSpectrograph(spectrograph, arm)
                              }
                              value={spectrograph}
                            />
                          }
                          label={id}
                        />
                      );
                    })}
                  </FormGroup>
                ))}
              </FormGroup>
            </Grid>
          </Grid>
        </FormControl>
        <Divider />
        <Typography style={styles.title} variant="headline" component="h2">
          Input/Output
        </Typography>
        <TextField
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
        <TextField
          label="Base Exposures"
          InputLabelProps={{
            shrink: true,
          }}
          helperText="Base exposures used by Exposure Generator"
          fullWidth
          margin="normal"
          value={this.state.baseExposures}
          onChange={evt => this.updateBaseExposures(evt.value)}
        />
        <TextField
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
