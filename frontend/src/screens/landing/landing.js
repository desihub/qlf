import React, { Component } from 'react';
import { withRouter } from 'react-router';
import PropTypes from 'prop-types';
import MainMenu from './widgets/main-menu/main-menu';
import Home from './widgets/home/home';
import AboutUs from './widgets/about/about';
import Help from './widgets/help/help';
import Tutorials from './widgets/tutorials/tutorials';
import ContactUs from './widgets/contact/contact';

const styles = {
  mainMenu: {
    height: '32px',
    backgroundColor: 'rgba(0, 0, 0, 0.87)',
    color: '#fff',
    padding: '0 24px 0 24px',
  },
  currentScreen: {
    minHeight: 'calc(100vh - 185px)',
  },
};

class Landing extends Component {
  static propTypes = {
    match: PropTypes.object.isRequired,
    location: PropTypes.object.isRequired,
    history: PropTypes.object.isRequired,
    updateUrl: PropTypes.func.isRequired,
  };

  renderMainMenu = () => {
    return <MainMenu currentScreen={this.props.history.location.pathname} />;
  };

  renderCurrentScreen = () => {
    switch (this.props.history.location.pathname) {
      case '/':
        return <Home updateUrl={this.props.updateUrl} />;
      case '/about':
        return <AboutUs />;
      case '/help':
        return <Help />;
      case '/tutorials':
        return <Tutorials />;
      case '/contact':
        return <ContactUs />;
      default:
        return null;
    }
  };

  render() {
    return (
      <div>
        <div style={styles.mainMenu}>{this.renderMainMenu()}</div>
        <div style={styles.currentScreen}>{this.renderCurrentScreen()}</div>
      </div>
    );
  }
}

const LandingWithRouter = withRouter(Landing);

export default LandingWithRouter;
