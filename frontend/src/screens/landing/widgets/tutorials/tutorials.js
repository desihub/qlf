import React from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
  },
  main: {
    width: '70vw',
    height: 'calc(100vh - 223px)',
    // overflowY: 'auto',
    margin: '16px',
    padding: '16px',
    hyphens: 'auto',
    wordWrap: 'break-word',
    fontSize: '1.2vw',
    lineHeight: 1.5,
    fontFamily: '"Helvetica Neue",Helvetica,Arial,sans-serif',
    fontWeight: 400,
  },
  link: {
    textDecoration: 'none',
  },
  gridRow: {
    display: 'grid',
    gridTemplateColumns: '12vw calc(70vw - 12vw)',
    width: '70vw',
    height: 'calc(100vh - 223px - 1.2vw - 2em - 3.15vh - 3.15vh)',
  },
  controlsContainer: {
    display: 'grid',
    width: '12vw',
    borderRight: '1px solid darkgrey',
    overflowY: 'auto',
    paddingRight: '10px',
    boxSizing: 'border-box',
  },
  viewer: {
    width: 'calc(70vw - 12vw)',
  },
  preview: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
  },
  iframe: {
    height: '70%',
    width: '80%',
  },
  title: {
    fontSize: '2em',
    margin: '3.15vh 0',
  },
};

class Tutorials extends React.Component {
  static propTypes = {
    classes: PropTypes.object,
  };

  renderControls = () => {
    const { classes } = this.props;
    return (
      <div className={classes.controlsContainer}>
        <p>Processing History</p>
      </div>
    );
  };

  renderViewer = () => {
    const { classes } = this.props;
    return (
      <div className={classes.preview}>
        <iframe
          src="https://www.youtube.com/embed/YLt5ouupWbk"
          frameBorder="0"
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          className={classes.iframe}
        />
        {/* <iframe
          width="560"
          height="315"
          src="https://www.youtube.com/embed/FT1T0OjvLO8"
          frameBorder="0"
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          className={classes.iframe}
        /> */}
      </div>
    );
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.container}>
        <Paper elevation={4} className={classes.main}>
          <h1 className={classes.title}>Tutorials</h1>
          <div className={classes.gridRow}>
            {this.renderControls()}
            <div className={classes.viewer}>{this.renderViewer()}</div>
          </div>
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(Tutorials);
