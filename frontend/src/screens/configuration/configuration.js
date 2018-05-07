import React from 'react';
import QLFApi from '../../containers/offline/connection/qlf-api';
import Paper from 'material-ui-next/Paper';
import TextField from 'material-ui-next/TextField';
import Divider from 'material-ui-next/Divider';
import Typography from 'material-ui-next/Typography';
import {
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
} from 'material-ui-next/Form';
import Checkbox from 'material-ui-next/Checkbox';
import _ from 'lodash';
import Button from 'material-ui-next/Button';

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

export default class Configuration extends React.Component {
  componentWillMount() {
    this.getCurrentConfiguration();
  }

  state = {
    name: '',
  };

  getCurrentConfiguration = async () => {
    const configuration = await QLFApi.getCurrentConfiguration();
    console.log(configuration);
  };

  render() {
    return (
      <div>
        <Paper style={styles.container} elevation={4}>
          <div style={styles.container}>
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
            />
            <FormControl component="fieldset">
              <FormLabel style={styles.label}>Arms to process</FormLabel>
              <FormGroup row>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={this.state.gilad}
                      // onChange={this.handleChange('gilad')}
                      value="gilad"
                    />
                  }
                  label="b"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={this.state.jason}
                      // onChange={this.handleChange('jason')}
                      value="jason"
                    />
                  }
                  label="r"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={this.state.antoine}
                      // onChange={this.handleChange('antoine')}
                      value="antoine"
                    />
                  }
                  label="z"
                />
              </FormGroup>
            </FormControl>
            <Divider />
            <FormControl component="fieldset">
              <FormLabel style={styles.label}>
                Spectrographs to process
              </FormLabel>
              <FormGroup row>
                {_.range(0, 10).map(id => {
                  return (
                    <FormControlLabel
                      control={
                        <Checkbox
                          checked={this.state.gilad}
                          // onChange={this.handleChange('gilad')}
                          value="gilad"
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
            />
            <Button variant="raised" color="default" style={styles.button}>
              Save
            </Button>
          </div>
        </Paper>
      </div>
    );
  }
}
