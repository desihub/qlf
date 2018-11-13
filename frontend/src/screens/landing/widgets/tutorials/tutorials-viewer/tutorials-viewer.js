import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  preview: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    height: '100%',
  },
  iframe: {
    height: '70%',
    width: '80%',
  },
};

class TutorialsViewer extends React.Component {
  static propTypes = {
    classes: PropTypes.object,
    loadEnd: PropTypes.func.isRequired,
    idVideo: PropTypes.string,
  };

  renderImage = () => {
    const { classes } = this.props;
    let url = '';

    if (this.props.idVideo !== '')
      url = `https://www.youtube.com/embed/${this.props.idVideo}`;

    if (url !== '')
      return (
        <iframe
          title="Vídeo"
          src={url}
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          frameBorder="0"
          onLoad={this.props.loadEnd}
          className={classes.iframe}
        />
      );
  };

  render() {
    const { classes } = this.props;
    return <div className={classes.preview}>{this.renderImage()}</div>;
  }
}

export default withStyles(styles)(TutorialsViewer);
