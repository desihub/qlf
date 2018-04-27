import React from 'react';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import AppBar from 'material-ui/AppBar';
import Landing from './screens/landing/landing';
import { Route } from 'react-router';
import { Provider } from 'react-redux';
import { store, history } from './store';
import Sidemenu from './screens/side-menu/side-menu';
import { ConnectedRouter } from 'react-router-redux';
import logo from './assets/DESILogo.png';
import OnlineContainer from './containers/online/online-container';
import OfflineContainer from './containers/offline/offline-container';

const styles = {
  headerTop: {
    fontSize: '35px',
    padding: '0px 6vw 35px 6vw',
    fontWeight: 900,
  },
  headerBottom: {
    fontSize: '15px',
  },
  logo: {
    height: '90px',
    paddingTop: '5px',
  },
  title: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  spanTitle: {
    alignSelf: 'flex-end',
  },
  bottom: {
    display: 'flex',
    justifyContent: 'space-between',
  },
};

class App extends React.Component {
  state = {
    openDrawer: false,
    url: '/',
    displayHeaders: true,
  };

  renderRouteName = () => {
    switch (history.location.pathname) {
      case '/monitor-realtime':
        return '- Monitor';
      case '/qa':
        return '- QA';
      case '/metrics':
        return '- Metrics';
      case '/qa-realtime':
        return '- QA Realtime';
      case '/metrics-realtime':
        return '- Metrics Realtime';
      case '/processing-history':
        return '- Processing History';
      case '/observing-history':
        return '- Observing History';
      default:
        return '';
    }
  };

  openDrawer = () => {
    this.setState({ openDrawer: true });
  };

  closeDrawer = url => {
    this.setState({ openDrawer: false, url });
  };

  updateUrl = url => {
    this.setState({ url });
  };

  showMenuIcon = () => {
    return false;
  };

  renderAppBar = () => {
    if (this.renderRouteName() === '') {
      return (
        <div style={styles.title}>
          <span style={styles.spanTitle}>DESI Quick Look</span>
          {window.innerWidth < 700 ? null : (
            <div>
              <img src={logo} alt={'logo'} style={styles.logo} />
            </div>
          )}
        </div>
      );
    } else {
      return (
        <div style={styles.title}>
          <span style={styles.spanTitle}>
            DESI Quick Look {this.renderRouteName()}
          </span>
          <span
            style={{ color: 'white', cursor: 'pointer', fontSize: '10px' }}
            onClick={this.toggleHeader}
          >
            Hide Menu
          </span>
        </div>
      );
    }
  };

  toggleHeader = () => {
    this.setState({ displayHeaders: !this.state.displayHeaders });
  };

  renderTopBar = () => {
    if (!this.state.displayHeaders) return;
    const homeAppleTitleStyle =
      this.renderRouteName() === '' ? styles.headerTop : null;
    return (
      <AppBar
        titleStyle={homeAppleTitleStyle}
        showMenuIconButton={this.showMenuIcon()}
        onLeftIconButtonTouchTap={this.openDrawer}
        title={this.renderAppBar()}
      />
    );
  };

  renderBottomBar = () => {
    if (!this.state.displayHeaders)
      return (
        <span
          style={{
            color: 'gray',
            marginRight: '1em',
            cursor: 'pointer',
            fontSize: '10px',
            display: 'flex',
            justifyContent: 'flex-end',
          }}
          onClick={this.toggleHeader}
        >
          Show Menu
        </span>
      );

    return (
      <AppBar
        showMenuIconButton={false}
        titleStyle={styles.headerBottom}
        title={this.renderBottomBarTitle()}
      />
    );
  };

  renderBottomBarTitle = () => {
    return (
      <div style={styles.bottom}>
        <span>© Copyright 2018, LIneA/DESI</span>
        <span>
          {process.env.REACT_APP_VERSION
            ? process.env.REACT_APP_VERSION.substring(0, 7)
            : ''}
        </span>
      </div>
    );
  };

  render() {
    return (
      <Provider store={store}>
        <ConnectedRouter history={history}>
          <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
            <div>
              {this.renderTopBar()}
              <Sidemenu
                openDrawer={this.state.openDrawer}
                closeDrawer={this.closeDrawer}
              />
              {['/', '/about', '/help', '/tutorials', '/contact'].map(path => (
                <Route
                  exact
                  key={path}
                  path={path}
                  render={() => <Landing updateUrl={this.updateUrl} />}
                />
              ))}
              <OnlineContainer />
              <OfflineContainer toggleHeader={this.toggleHeader} />
              {this.renderBottomBar()}
            </div>
          </MuiThemeProvider>
        </ConnectedRouter>
      </Provider>
    );
  }
}

export default App;
