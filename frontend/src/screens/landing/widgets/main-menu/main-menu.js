import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

const styles = {
  link: {
    textDecoration: 'none',
    color: 'white',
    fontSize: '15px',
    fontWeight: '100',
    lineHeight: '32px',
    paddingRight: '10px',
    paddingLeft: '10px',
  },
  currentLink: {
    fontStyle: 'italic',
    boxShadow: '0px -4px 0px white inset',
  },
  mainMenu: {
    display: 'flex',
    padding: '0px 0px 0px 5vw',
  },
};

export default class MainMenu extends React.Component {
  static propTypes = {
    currentScreen: PropTypes.string,
  };

  menuStyle = screen => {
    const selected = { ...styles.currentLink, ...styles.link };
    switch (this.props.currentScreen) {
      case '/':
        return screen === 'home' ? selected : styles.link;
      case '/about':
        return screen === 'about' ? selected : styles.link;
      case '/help':
        return screen === 'help' ? selected : styles.link;
      case '/tutorials':
        return screen === 'tutorials' ? selected : styles.link;
      case '/contact':
        return screen === 'contact' ? selected : styles.link;
      default:
        return styles.link;
    }
  };

  render() {
    return (
      <div style={styles.mainMenu}>
        <Link style={this.menuStyle('home')} to="/">
          Home
        </Link>
        <Link style={this.menuStyle('about')} to="/about">
          About Us
        </Link>
        <Link style={this.menuStyle('help')} to="/help">
          Help
        </Link>
        <Link style={this.menuStyle('tutorials')} to="/tutorials">
          Tutorials
        </Link>
        <Link style={this.menuStyle('contact')} to="/contact">
          Contact Us
        </Link>
        <a
          target="_blank" // eslint-disable-line
          style={this.menuStyle('releases')}
          href="https://github.com/desihub/qlf/releases"
        >
          Releases
        </a>
      </div>
    );
  }
}
