import React from 'react';
import Modal from '@material-ui/core/Modal';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import { FadeLoader } from 'halogenium';
import TextField from '@material-ui/core/TextField';
import Icon from '@material-ui/core/Icon';

const styles = {
  modalBody: {
    position: 'absolute',
    backgroundColor: 'white',
    boxShadow: 1,
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  iframe: {
    height: '60vh',
    width: '70vw',
  },
  controls: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    width: '80%',
    minWidth: 400,
    justifyContent: 'space-evenly',
  },
  radioGroup: {
    display: 'flex',
    flexDirection: 'row',
  },
  button: {
    float: 'right',
  },
};

class CommentModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      comment: '',
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    handleClose: PropTypes.func.isRequired,
  };

  handleChange = name => evt => {
    this.setState({
      [name]: evt.target.value,
    });
  };

  loadStart = () => {
    this.setState({ loading: true });
  };

  loadEnd = () => {
    this.setState({ loading: false });
  };

  renderLoading = () => {
    if (!this.state.loading) return null;
    return (
      <div style={{ ...styles.loading }}>
        <FadeLoader color="#424242" size="16px" margin="4px" />
      </div>
    );
  };

  render() {
    const { classes } = this.props;
    return (
      <Modal className={classes.modal} open={true} onClose={this.handleClose}>
        <div className={classes.modalBody}>
          <TextField
            id="Comment"
            label="Comment"
            // className={classes.textField}
            value={this.state.comment}
            onChange={this.handleChange('comment')}
            margin="normal"
          />
          <Icon>send</Icon>
          {this.renderLoading()}
        </div>
      </Modal>
    );
  }
}

export default withStyles(styles)(CommentModal);
