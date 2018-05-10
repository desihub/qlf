import React from 'react';
import Paper from 'material-ui-next/Paper';
import Typography from 'material-ui-next/Typography';

const styles = {
  paper: {
    margin: '2em',
    textAlign: 'center',
  },
  typo: {
    padding: '1em',
  },
};

export default class UnderConstruction extends React.Component {
  render() {
    return (
      <Paper style={styles.paper} elevation={4}>
        <Typography style={styles.typo} variant="headline" component="h3">
          Under Construction.
        </Typography>
        <Typography style={styles.typo} component="p">
          This app is not implemented yet.
        </Typography>
      </Paper>
    );
  }
}
