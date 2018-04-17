import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import PropTypes from 'prop-types';
import Terminal from '../terminal/terminal';

const styles = {
  dialog: {
    height: '100%',
    maxWidth: '90%',
    width: '90%',
  },
  terminal: {
    height: '80%',
  },
  close: {
    float: 'right',
    cursor: 'pointer',
  },
};

export default class CameraDialog extends React.Component {
  static propTypes = {
    openDialog: PropTypes.bool.isRequired,
    closeDialog: PropTypes.func.isRequired,
    cameraIndex: PropTypes.number.isRequired,
    lines: PropTypes.array.isRequired,
  };

  renderTitle = () => {
    return (
      <div>
        <span style={styles.close} onClick={this.props.closeDialog}>
          x
        </span>
        <span>{`Camera ${this.props.cameraIndex}`}</span>
      </div>
    );
  };

  render() {
    const actions = [
      <FlatButton
        key={1}
        label="Close"
        primary={true}
        keyboardFocused={false}
        onClick={this.props.closeDialog}
      />,
    ];

    return (
      <div>
        <Dialog
          title={this.renderTitle()}
          actions={actions}
          modal={false}
          open={this.props.openDialog}
          onRequestClose={this.props.closeDialog}
          contentStyle={styles.dialog}
        >
          <Terminal height={'400px'} lines={this.props.lines} />
        </Dialog>
      </div>
    );
  }
}
