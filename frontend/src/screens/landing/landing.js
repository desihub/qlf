import React, { Component } from 'react';
import { withRouter } from 'react-router';
import PropTypes from 'prop-types';
import AppBar from 'material-ui/AppBar';
import MainMenu from './widgets/main-menu/main-menu';
import Home from './widgets/home/home';
import AboutUs from './widgets/about/about';
import Help from './widgets/help/help';
import ContactUs from './widgets/contact/contact';

const styles = {
  mainMenu: {
    height: '32px',
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
      case '/contact':
        return <ContactUs />;
      default:
        return null;
    }
  };

  render() {
    return (
      <div>
        <AppBar
          showMenuIconButton={false}
          style={styles.mainMenu}
          title={this.renderMainMenu()}
          zDepth={0}
        />
        {this.renderCurrentScreen()}
      </div>
    );
  }
}

const LandingWithRouter = withRouter(Landing);

export default LandingWithRouter;
