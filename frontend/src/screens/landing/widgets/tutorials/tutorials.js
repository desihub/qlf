import React from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import { FadeLoader } from 'halogenium';
import TutorialsViewer from './tutorials-viewer/tutorials-viewer';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import Icon from '@material-ui/core/Icon';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
  },
  main: {
    width: '70vw',
    height: 'calc(100vh - 223px)',
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
    width: '12vw',
    borderRight: '1px solid darkgrey',
    overflow: 'auto',
    paddingRight: '10px',
    boxSizing: 'border-box',
  },
  viewer: {
    width: 'calc(70vw - 12vw)',
    position: 'relative',
  },
  title: {
    fontSize: '2em',
    margin: '3.15vh 0',
  },
  text: {
    fontSize: '1.2vw',
  },
  textItem: {
    fontSize: '1vw',
    cursor: 'pointer',
    display: 'block',
    textAlign: 'center',
    borderBottom: '1px solid #333',
    width: '100%',
    paddingBottom: '3px',
  },
  fadeLoaderFull: {
    position: 'absolute',
    paddingLeft: 'calc((100vw - 40px) / 2)',
    paddingTop: 'calc(22vh)',
  },
  fadeLoader: {
    position: 'absolute',
    paddingLeft: 'calc(70vw - 41vw)',
    paddingTop: 'calc(22vh)',
  },
  space: {
    paddingBottom: '8px',
  },
};

class Tutorials extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      idVideo: '',
    };
  }

  static propTypes = {
    classes: PropTypes.object.isRequired,
  };

  loadStart = () => {
    this.setState({ loading: true });
  };

  loadEnd = () => {
    this.setState({ loading: false });
  };

  handleClickVideo = idVideo => {
    this.setState({ idVideo });
    if (this.state.idVideo !== idVideo) this.loadStart();
  };

  renderLoading = () => {
    if (!this.state.loading) return null;
    const showControls = this.state.idVideo;
    const classLoading = showControls
      ? styles.fadeLoader
      : styles.fadeLoaderFull;
    if (this.state.idVideo !== '') {
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
    }
  };

  renderControls = () => {
    const { classes } = this.props;
    return (
      <div className={classes.controlsContainer}>
        <ExpansionPanel>
          <ExpansionPanelSummary expandIcon={<Icon>expand_more</Icon>}>
            <Typography className={classes.text}>Processing History</Typography>
          </ExpansionPanelSummary>
          <div onClick={() => this.handleClickVideo('YLt5ouupWbk')}>
            <ExpansionPanelDetails className={classes.space}>
              <Typography className={classes.textItem}>QA</Typography>
            </ExpansionPanelDetails>
          </div>
          <div onClick={() => this.handleClickVideo('FT1T0OjvLO8')}>
            <ExpansionPanelDetails>
              <Typography className={classes.textItem}>View</Typography>
            </ExpansionPanelDetails>
          </div>
        </ExpansionPanel>
      </div>
    );
  };

  renderViewer = () => {
    return (
      <TutorialsViewer idVideo={this.state.idVideo} loadEnd={this.loadEnd} />
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
            <div className={classes.viewer}>
              {this.renderLoading()}
              {this.renderViewer()}
            </div>
          </div>
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(Tutorials);
