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
import Fade from '@material-ui/core/Fade';
import Typography from '@material-ui/core/Typography';

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
    width: '80vw',
    maxHeight: '80vh',
    overflowY: 'scroll',
    animationDuration: '2s',
  },
  primaryText: {
    wordBreak: 'break-word',
  },
  commentControls: {
    display: 'flex',
  },
  hiddenControls: {
    display: 'none',
  },
  icon: {
    cursor: 'pointer',
  },
  deleteTitle: {
    color: 'red',
    paddingBottom: 10,
  },
  deleteBody: {
    wordBreak: 'break-word',
  },
};

class CommentModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      comment: '',
      editedComment: '',
      comments: undefined,
      selectedComment: undefined,
      editCommentId: undefined,
      deleteComment: false,
      confirmCommentToDelete: undefined,
      deleteId: undefined,
    };
  }

  static propTypes = {
    classes: PropTypes.object,
    handleClose: PropTypes.func.isRequired,
    processId: PropTypes.number.isRequired,
    readOnly: PropTypes.bool.isRequired,
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

  hoverComment = selectedComment => {
    this.setState({ selectedComment });
  };

  hoverCommentEnd = () => {
    this.setState({ selectedComment: undefined });
  };

  renderComments = () => {
    const { classes } = this.props;
    if (!this.state.comments) return null;
    return (
      <div className={classes.list}>
        {this.props.readOnly ? (
          <Typography variant="title" id="modal-title">
            Comments
          </Typography>
        ) : null}
        <List>
          {this.state.comments.map(comment => {
            return (
              <div key={comment.id}>
                <ListItem
                  onMouseEnter={() => this.hoverComment(comment.id)}
                  onMouseLeave={this.hoverCommentEnd}
                >
                  {this.renderOrEditComment(comment)}
                  {this.renderCommentControls(comment)}
                </ListItem>
                <Divider />
              </div>
            );
          })}
        </List>
      </div>
    );
  };

  renderCommentControls = comment => {
    if (this.props.readOnly) return null;
    const { classes } = this.props;
    const selected = this.state.selectedComment === comment.id;
    return this.state.editCommentId !== comment.id ? (
      <Fade in={selected}>
        <div>
          <Icon
            className={classes.icon}
            onClick={() => this.editComment(comment.id, comment.text)}
          >
            edit
          </Icon>
          <Icon
            className={classes.icon}
            onClick={() => this.deleteComment(comment.id, comment.text)}
          >
            delete
          </Icon>
        </div>
      </Fade>
    ) : (
      <Fade in={true} className={classes.commentControls}>
        <div>
          <Icon className={classes.icon} onClick={this.updateComment}>
            save
          </Icon>
          <Icon className={classes.icon} onClick={this.clearEdit}>
            cancel
          </Icon>
        </div>
      </Fade>
    );
  };

  deleteComment = (id, comment) => {
    this.setState({
      confirmCommentToDelete: comment,
      deleteComment: true,
      deleteId: id,
    });
  };

  renderOrEditComment = comment => {
    const { classes } = this.props;
    return this.state.editCommentId === comment.id ? (
      <TextField
        id="Comment"
        label="Edit Comment"
        className={classes.textField}
        value={this.state.editedComment}
        onChange={this.handleChange('editedComment')}
        fullWidth
        onKeyPress={this.handleEnterPressedUpdateComment}
      />
    ) : (
      <ListItemText
        classes={{ primary: classes.primaryText }}
        primary={comment.text}
        secondary={comment.date}
      />
    );
  };

  handleEnterPressedUpdateComment = e => {
    if (e.key === 'Enter') {
      this.updateComment();
    }
  };

  clearEdit = () => {
    this.setState({ editCommentId: undefined, editedComment: undefined });
  };

  editComment = (editCommentId, comment) => {
    this.setState({ editCommentId, editedComment: comment });
  };

  updateComment = async () => {
    if (this.state.editedComment === '') return;
    const comment = await QlfApi.updateProcessComment(
      this.state.editCommentId,
      this.props.processId,
      this.state.editedComment
    );
    if (comment.id) {
      this.clearEdit();
      this.fetchComments();
    }
  };

  renderDeleteConfirmation = () => (
    <Modal
      className={this.props.classes.modal}
      open={this.state.deleteComment}
      onClose={this.closeDeleteCommentDialog}
    >
      <div className={this.props.classes.modalBody}>
        <Typography
          className={this.props.classes.deleteTitle}
          variant="title"
          id="modal-title"
        >
          Are you sure you want to delete
        </Typography>
        <Typography
          className={this.props.classes.deleteBody}
          variant="body2"
          id="simple-modal-description"
        >
          {this.state.confirmCommentToDelete}
        </Typography>
        <div>
          <Button
            onClick={this.deleteCommentConfirm}
            variant="flat"
            size="small"
            className={this.props.classes.button}
          >
            ok
          </Button>
          <Button
            onClick={this.closeDeleteCommentDialog}
            variant="flat"
            size="small"
            className={this.props.classes.button}
          >
            cancel
          </Button>
        </div>
      </div>
    </Modal>
  );

  closeDeleteCommentDialog = () => {
    this.setState({ deleteComment: false, deleteId: undefined });
  };

  deleteCommentConfirm = async () => {
    await QlfApi.deleteProcessComment(this.state.deleteId);
    this.closeDeleteCommentDialog();
    this.fetchComments();
  };

  renderAddComment = () => {
    if (this.props.readOnly) return null;
    const { classes } = this.props;
    return (
      <div className={classes.inline}>
        <TextField
          id="Comment"
          label="Comment"
          className={classes.textField}
          value={this.state.comment}
          onChange={this.handleChange('comment')}
          fullWidth
          onKeyPress={this.handleEnterPressedAddComment}
        />
        <Icon className={classes.icon} onClick={this.addComment}>
          send
        </Icon>
      </div>
    );
  };

  addComment = async () => {
    if (this.state.comment === '') return;
    const comment = await QlfApi.addProcessComment(
      this.state.comment,
      this.props.processId
    );
    if (comment.id) {
      this.setState({ comment: '' });
      this.fetchComments();
    }
  };

  handleEnterPressedAddComment = e => {
    if (e.key === 'Enter') {
      this.addComment();
    }
  };

  render() {
    const { classes } = this.props;
    return (
      <Modal
        className={classes.modal}
        open={true}
        onClose={this.props.handleClose}
      >
        <div className={classes.modalBody}>
          {this.renderDeleteConfirmation()}
          {this.renderAddComment()}
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
