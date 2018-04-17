import React from 'react';
import TextField from 'material-ui/TextField';
import Recaptcha from 'react-recaptcha';
import RaisedButton from 'material-ui/RaisedButton';
import QlfApi from '../../../../containers/offline/connection/qlf-api';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
  },
  main: {
    maxWidth: '800px',
    flexDirection: 'column',
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

  storeNameRef = ref => {
    this.nameRef = ref;
  };

  storeEmailRef = ref => {
    this.emailRef = ref;
  };

  storeSubjectRef = ref => {
    this.subjectRef = ref;
  };

  storeMessageRef = ref => {
    this.messageRef = ref;
  };

  sendEmail = () => {
    const required = 'Required';
    const invalid = 'Invalid email';
    const name = this.nameRef.getValue();
    const message = this.messageRef.getValue();
    const email = this.emailRef.getValue();
    const subject = this.subjectRef.getValue();
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
        nameError: name ? '' : required,
        messageError: message ? '' : required,
        emailError: regex.test(email) ? '' : invalid,
        subjectError: subject ? '' : required,
      });
    }
  };

  render() {
    return (
      <div style={styles.container}>
        <div style={styles.main}>
          <h1>Contact Us</h1>
          <TextField
            ref={ref => this.storeNameRef(ref)}
            fullWidth={true}
            floatingLabelText="Name"
            errorText={this.state.nameError}
          />
          <TextField
            ref={ref => this.storeEmailRef(ref)}
            fullWidth={true}
            floatingLabelText="Email"
            errorText={this.state.emailError}
          />
          <TextField
            ref={ref => this.storeSubjectRef(ref)}
            fullWidth={true}
            floatingLabelText="Subject"
            errorText={this.state.subjectError}
          />
          <TextField
            ref={ref => this.storeMessageRef(ref)}
            floatingLabelText="Message"
            multiLine={true}
            rows={4}
            fullWidth={true}
            errorText={this.state.messageError}
          />
          <Recaptcha
            sitekey={process.env.REACT_APP_CAPTCHA_KEY}
            render="explicit"
            verifyCallback={this.verifyCallback}
          />
          <RaisedButton
            label="submit"
            style={{ margin: '1em' }}
            labelStyle={{ color: 'white' }}
            backgroundColor={'#00C853'}
            fullWidth={true}
            onClick={this.sendEmail}
          />
        </div>
      </div>
    );
  }
}
