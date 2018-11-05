import React from 'react';
import Recaptcha from 'react-recaptcha';
import Button from '@material-ui/core/Button';
import QlfApi from '../../../../containers/offline/connection/qlf-api';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
  },
  main: {
    width: '70vw',
    flexDirection: 'column',
    height: 'calc(100vh - 223px)',
    overflowY: 'auto',
    margin: '16px',
    padding: '16px',
    fontSize: '1.2vw',
  },
  text: {
    fontSize: '1.2vw',
    marginBottom: '20px',
  },
  button: {
    backgroundColor: 'rgb(0, 200, 83)',
    fontSize: '1.1vw',
    color: '#fff',
    marginTop: '20px',
  },
};

export default class ContactUs extends React.Component {
  state = {
    nameError: undefined,
    emailError: undefined,
    subjectError: undefined,
    messageError: undefined,
    validationError: undefined,
  };

  verifyCallback = () => {
    this.setState({ validation: true });
  };

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  sendEmail = () => {
    const name = this.state.name;
    const message = this.state.message;
    const email = this.state.email;
    const subject = this.state.subject;
    const regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (
      regex.test(email) &&
      message &&
      subject &&
      name &&
      this.state.validation
    ) {
      QlfApi.sendTicketMail(email, message, subject, name);
    } else {
      this.setState({
        nameError: name === undefined,
        messageError: message === undefined,
        emailError: !regex.test(email),
        subjectError: subject === undefined,
      });
    }
  };

  render() {
    return (
      <div style={styles.container}>
        <Paper elevation={4} style={styles.main}>
          <h1>Contact Us</h1>
          <TextField
            fullWidth={true}
            label="Name"
            onChange={this.handleChange('name')}
            error={this.state.nameError}
            style={styles.text}
          />
          <TextField
            fullWidth={true}
            label="Email"
            onChange={this.handleChange('email')}
            error={this.state.emailError}
            style={styles.text}
          />
          <TextField
            fullWidth={true}
            label="Subject"
            onChange={this.handleChange('subject')}
            error={this.state.subjectError}
            style={styles.text}
          />
          <TextField
            label="Message"
            multiline={true}
            rows={4}
            fullWidth={true}
            onChange={this.handleChange('message')}
            error={this.state.messageError}
            style={styles.text}
          />
          <Recaptcha
            sitekey={process.env.REACT_APP_CAPTCHA_KEY}
            render="explicit"
            verifyCallback={this.verifyCallback}
          />
          <Button
            labelstyle={{ color: 'white', fontSize: '1.1vw' }}
            color="primary"
            fullWidth={true}
            onClick={this.sendEmail}
            style={styles.button}
          >
            Submit
          </Button>
        </Paper>
      </div>
    );
  }
}
