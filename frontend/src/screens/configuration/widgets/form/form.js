import React from 'react';
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
import InputAdornment from '@material-ui/core/InputAdornment';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import { configMap } from './configuration-map';
import QlfApi from '../../../../containers/offline/connection/qlf-api';

const styles = {
  container: {
    margin: '1em',
  },
  label: {
    fontSize: '0.75rem',
    marginTop: 16,
  },
  title: {
    marginTop: 16,
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
  labelThreshold: {
    fontSize: '0.75rem',
    marginTop: 0,
  },
  threshold: {
    display: 'flex',
    flexDirection: 'column',
    alignItens: 'left',
    padding: 8,
    width: 70,
  },
};

class Form extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      night: '',
      arms: [],
      input: '',
      output: '',
      exposures: '',
      qlconfig: '',
      spectrographs: [],
      loading: false,
      maxWorkers: '',
      diskAlert: 20,
      diskWarning: 80,
      calibrationPath: '',
    };
  }

  componentDidMount() {
    this.getCurrentConfiguration();
  }

  static propTypes = {
    classes: PropTypes.object,
    daemonRunning: PropTypes.bool.isRequired,
  };

  updateArm = arm => {
    if (this.state.arms.includes(arm)) {
      this.setState({
        arms: this.state.arms.filter(a => a !== arm),
        spectrographs: [],
      });
    } else {
      this.setState({
        arms: this.state.arms.concat(arm),
        spectrographs: _.range(0, 10),
      });
    }
  };

  updateSpectrograph = (arm, spectrograph) => {
    if (!this.state.arms.includes(arm)) {
      this.setState({
        arms: this.state.arms.concat(arm),
      });
    }

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

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  getCurrentConfiguration = async () => {
    this.setState({ loading: true });
    const configuration = await QlfApi.getCurrentConfiguration();
    const thresholds = await QlfApi.getCurrentThresholds();
    this.updateThresholds(thresholds);
    this.setState({ loading: false });
    this.updateConfiguration(configuration);
  };

  getDefaultConfiguration = async () => {
    this.setState({ loading: true });
    await QlfApi.getDefaultConfiguration();
    const configuration = await QlfApi.getCurrentConfiguration();
    const thresholds = await QlfApi.getCurrentThresholds();
    this.updateThresholds(thresholds);
    this.setState({ loading: false });
    this.updateConfiguration(configuration);
  };

  updateConfiguration = configuration => {
    if (configuration && configuration.results) {
      const {
        allowed_delay,
        arms,
        desi_spectro_data,
        desi_spectro_redux,
        exposures,
        spectrographs,
        calibration_path,
        max_workers,
      } = configuration.results;

      const specs = spectrographs.split(',').map(s => parseInt(s, 10));

      this.setState({
        arms: arms.split(','),
        input: desi_spectro_data,
        output: desi_spectro_redux,
        exposures: exposures,
        spectrographs: specs,
        allowedDelay: allowed_delay,
        calibrationPath: calibration_path,
        maxWorkers: max_workers,
      });
    }
  };

  updateThresholds = thresholds => {
    if (thresholds && thresholds.disk_percent_alert)
      this.setState({
        diskAlert: thresholds.disk_percent_alert,
        diskWarning: thresholds.disk_percent_warning,
      });
  };

  saveConfiguration = async () => {
    this.setState({ loading: true });
    const values = [],
      keys = [];
    configMap.forEach(config => {
      const value = Array.isArray(this.state[config.state])
        ? this.state[config.state].join(',')
        : this.state[config.state];
      values.push(value);
      keys.push(config.api);
    });
    // await QlfApi.editConfiguration(keys, values);
    this.setState({ loading: false });
  };

  render() {
    return (
      <div style={styles.container}>
        {this.state.loading ? <CircularProgress size={50} /> : null}
        <Typography style={styles.title} variant="headline" component="h2">
          Workers
        </Typography>
        {configMap.filter(c => c.type === 'workers').map(c => (
          <TextField
            disabled={true}
            key={c.label}
            label={c.label}
            InputLabelProps={{
              shrink: true,
            }}
            helperText={c.helperText}
            fullWidth
            margin="normal"
            value={this.state[c.state]}
            onChange={this.handleChange(c.state)}
          />
        ))}
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
                  selected={
                    this.state.arms.includes(arm)
                      ? this.state.spectrographs
                      : []
                  }
                  onClick={spectrograph =>
                    this.updateSpectrograph(arm, spectrograph)
                  }
                  size={100}
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      disabled={true}
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
        {configMap.filter(c => c.type === 'io').map(c => (
          <TextField
            disabled={true}
            key={c.label}
            label={c.label}
            InputLabelProps={{
              shrink: true,
            }}
            helperText={c.helperText}
            fullWidth
            margin="normal"
            value={this.state[c.state]}
            onChange={this.handleChange(c.state)}
          />
        ))}
        <FormLabel style={styles.label}>Threshold Values</FormLabel>
        <Paper style={styles.threshold} elevation={2}>
          <FormLabel style={styles.labelThreshold}>Disk Space</FormLabel>
          {configMap.filter(c => c.type === 'thresholds').map(c => (
            <TextField
              disabled={true}
              key={c.label}
              label={c.label}
              type="number"
              InputLabelProps={{
                shrink: true,
              }}
              inputProps={{
                min: 0,
                max: 100,
                step: 10,
              }}
              margin="normal"
              value={this.state[c.state]}
              onChange={this.handleChange(c.state)}
          InputProps={{ // eslint-disable-line
                endAdornment: <InputAdornment position="end">%</InputAdornment>,
              }}
            />
          ))}
        </Paper>
        <Button
          onClick={this.saveConfiguration}
          disabled={true}
          variant="raised"
          color="default"
          style={styles.button}
        >
          Save
        </Button>
        <Button
          onClick={this.getDefaultConfiguration}
          disabled={true}
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

export default withStyles(styles)(Form);
