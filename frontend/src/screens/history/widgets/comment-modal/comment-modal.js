import React from 'react';
import Modal from '@material-ui/core/Modal';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import { FadeLoader } from 'halogenium';
import TextField from '@material-ui/core/TextField';
import Icon from '@material-ui/core/Icon';
import QlfApi from '../../../../containers/offline/connection/qlf-api';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';

const styles = {
  modalBody: {
    position: 'absolute',
    backgroundColor: 'white',
    boxShadow: 1,
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    minHeight: 80,
    maxWidth: '80vw',
  },
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  textField: {
    marginTop: 0,
  },
  inline: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    minWidth: '80vw',
  },
  list: {
    maxWidth: '80vw',
    maxHeight: '80vh',
    overflowY: 'scroll',
  },
  primaryText: {
    wordBreak: 'break-all',
  },
};

class CommentModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      comment: '',
      comments: undefined,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    handleClose: PropTypes.func.isRequired,
    processId: PropTypes.number.isRequired,
  };

  componentWillMount() {
    this.fetchComments();
  }

  fetchComments = async () => {
    this.loadStart();
    const comments = await QlfApi.getProcessComments(this.props.processId);
    this.loadEnd();
    if (comments && comments.results)
      this.setState({ comments: comments.results });
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

  renderComments = () => {
    const { classes } = this.props;
    if (!this.state.comments) return null;
    return (
      <div className={classes.list}>
        <List>
          {this.state.comments.map(comment => (
            <div key={comment.id}>
              <ListItem>
                <ListItemText
                  classes={{ primary: classes.primaryText }}
                  primary={comment.comment}
                  secondary={comment.date}
                />
              </ListItem>
              <Divider />
            </div>
          ))}
        </List>
      </div>
    );
  };

  render() {
    const { classes } = this.props;
    return (
      <Modal className={classes.modal} open={true} onClose={this.handleClose}>
        <div className={classes.modalBody}>
          <div className={classes.inline}>
            <TextField
              id="Comment"
              label="Comment"
              className={classes.textField}
              value={this.state.comment}
              onChange={this.handleChange('comment')}
              fullWidth
            />
            <Icon>send</Icon>
          </div>
          {this.renderComments()}
          {this.renderLoading()}
          <Button
            onClick={this.props.handleClose}
            variant="flat"
            size="small"
            className={classes.button}
          >
            close
          </Button>
        </div>
      </Modal>
    );
  }
}

export default withStyles(styles)(CommentModal);
