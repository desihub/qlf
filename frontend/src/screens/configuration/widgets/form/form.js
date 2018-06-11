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
import Petals from '../../../../components/petals/petals';

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
  formGroup: {
    display: 'flex',
    flexDirection: 'row',
    paddingTop: 16,
    justifyContent: 'space-around',
    width: '90vw',
  },
  formDiv: {
    display: 'grid',
  },
  formCheckbox: {
    margin: 0,
    justifySelf: 'center',
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
    spectrographs: { b: [], r: [], z: [] },
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
    const newArm = {};
    if (this.state.arms.includes(arm)) {
      newArm[arm] = [];
      this.setState({
        arms: this.state.arms.filter(a => a !== arm),
        spectrographs: Object.assign(this.state.spectrographs, newArm),
      });
    } else {
      newArm[arm] = _.range(0, 10);
      this.setState({
        arms: this.state.arms.concat(arm),
        spectrographs: Object.assign(this.state.spectrographs, newArm),
      });
    }
  };

  updateSpectrograph = (arm, spectrograph) => {
    const newArm = {};
    if (this.state.spectrographs[arm].includes(spectrograph)) {
      newArm[arm] = this.state.spectrographs[arm].filter(
        s => s !== spectrograph
      );
      this.setState({
        spectrographs: Object.assign(this.state.spectrographs, newArm),
      });
    } else {
      newArm[arm] = this.state.spectrographs[arm].concat(spectrograph);
      this.setState({
        spectrographs: Object.assign(this.state.spectrographs, newArm),
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

      const specs = spectrographs.split(',').map(s => parseInt(s, 10));

      const spectrographsObj = {
        b: arms.includes('b') ? specs : [],
        r: arms.includes('r') ? specs : [],
        z: arms.includes('z') ? specs : [],
      };

      this.setState({
        arms: arms.split(','),
        input: desi_spectro_data,
        output: desi_spectro_redux,
        exposures: exposures,
        qlconfig: qlconfig,
        spectrographs: spectrographsObj,
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
          <FormLabel style={styles.label}>
            Arms / Spectrographs to process
          </FormLabel>
          <FormGroup style={styles.formGroup}>
            {['b', 'r', 'z'].map(arm => (
              <div key={arm} style={styles.formDiv}>
                <Petals
                  selected={this.state.spectrographs[arm]}
                  onClick={spectrograph =>
                    this.updateSpectrograph(arm, spectrograph)
                  }
                  size={100}
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={this.state.arms.includes(arm)}
                      onChange={() => this.updateArm(arm)}
                      value={arm}
                    />
                  }
                  label={arm}
                  style={styles.formCheckbox}
                />
              </div>
            ))}
          </FormGroup>
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
