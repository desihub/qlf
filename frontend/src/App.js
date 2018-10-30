import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import AppBar from 'material-ui/AppBar';
import Landing from './screens/landing/landing';
import { Route } from 'react-router';
import { Provider } from 'react-redux';
import { store, history } from './store';
import { ConnectedRouter } from 'react-router-redux';
import logo from './assets/DESILogo.png';
import logoLinea from './assets/linea-logo-mini.png';
import OnlineContainer from './containers/online/online-container';
import OfflineContainer from './containers/offline/offline-container';
import Icon from '@material-ui/core/Icon';
import Notification from './components/notification/notification';

const theme = {
  spacing: {
    iconSize: 24,
    desktopGutter: 24,
    desktopGutterMore: 32,
    desktopGutterLess: 16,
    desktopGutterMini: 8,
    desktopKeylineIncrement: 64,
    desktopDropDownMenuItemHeight: 32,
    desktopDropDownMenuFontSize: 15,
    desktopDrawerMenuItemHeight: 48,
    desktopSubheaderHeight: 48,
    desktopToolbarHeight: 56,
  },
  fontFamily: 'Roboto, sans-serif',
  borderRadius: 2,
  palette: {
    primary1Color: '#24292E',
    primary2Color: '#0097a7',
    primary3Color: '#bdbdbd',
    accent1Color: '#ba000d',
    accent2Color: '#f5f5f5',
    accent3Color: '#9e9e9e',
    textColor: 'rgba(0, 0, 0, 0.87)',
    secondaryTextColor: 'rgba(0, 0, 0, 0.84)',
    alternateTextColor: '#ffffff',
    canvasColor: '#ffffff',
    borderColor: '#e0e0e0',
    disabledColor: 'rgba(0, 0, 0, 0.3)',
    pickerHeaderColor: '#24292E',
    clockCircleColor: 'rgba(0, 0, 0, 0.07)',
    shadowColor: 'rgba(0, 0, 0, 1)',
  },
};

const styles = {
  grid: {
    display: 'grid',
    gridTemplateRows: '38px auto 28px',
    gridTemplateColumns: 'auto',
    height: '100vh',
    width: '100vw',
    position: 'relative',
  },
  headerContainer: {
    position: 'relative',
    height: '99px',
  },
  headerTop: {
    fontSize: '35px',
    padding: '0px 6vw 35px 6vw',
    fontWeight: 900,
  },
  headerTitleBottom: {
    fontSize: '16px',
    height: '28px',
    lineHeight: '28px',
  },
  logo: {
    height: '90px',
  },
  logoLinea: {
    verticalAlign: 'middle',
    cursor: 'pointer',
  },
  logoDesi: {
    position: 'absolute',
    top: '50%',
    right: '100px',
    zIndex: 1250,
    marginTop: '-31px',
  },
  title: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  spanTitle: {
    alignSelf: 'flex-end',
  },
  smallTitle: {
    fontSize: 18,
    lineHeight: '38px',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  smallSpanTitle: {
    alignSelf: 'flex-end',
  },
  headerTopSmall: {
    height: '38px',
  },
  hideMenu: { color: 'white', cursor: 'pointer', fontSize: '10px' },
  bottom: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '0.9rem',
  },
  homeIcon: {
    fontSize: 20,
    alignSelf: 'center',
    paddingRight: '8px',
    cursor: 'pointer',
  },
  footerRight: {
    display: 'flex',
    alignItems: 'center',
  },
  connected: {
    fontSize: 16,
    color: 'green',
    paddingLeft: 8,
  },
  disconnected: {
    fontSize: 16,
    color: 'red',
    paddingLeft: 8,
  },
  footerContainer: {
    width: '100%',
    position: 'fixed',
    bottom: '0',
    left: '0',
  },
};

class App extends React.Component {
  state = {
    url: '/',
    displayHeaders: true,
    websocketConnected: false,
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
      case '/configuration':
        return '- Configuration';
      case '/observing-history':
        return '- Observing History';
      case '/afternoon-planning':
        return '- Afternoon Planning';
      case '/survey-report':
        return '- Survey Report';
      case '/camera-log':
        return '- Camera Log';
      case '/camera-log-realtime':
        return '- Camera Log';
      case '/ccd-viewer':
        return '- CCD Viewer';
      case '/log-viewer':
        return '- Log Viewer';
      case '/fiber-viewer':
        return '- Fiber Viewer';
      case '/spectra-viewer':
        return '- Spectra Viewer';
      case '/under-construction':
        return '- Under Construction';
      case '/focus-viewer':
        return '- Focus Viewer';
      case '/snr-viewer':
        return '- SNR Viewer';
      case '/trend-analysis':
        return '- Trend Analysis';
      case '/observing-conditions':
        return '- Observing Conditions';
      default:
        return '';
    }
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
        </div>
      );
    } else {
      return (
        <div style={styles.smallTitle}>
          <span style={styles.smallSpanTitle}>
            DESI Quick Look {this.renderRouteName()}
          </span>
          <div style={{ display: 'flex' }}>
            {history.location.pathname === '/monitor-realtime' ? (
              <Notification />
            ) : null}
            <Icon
              onClick={() => window.open('/', 'home', 'width=950, height=650')}
              style={styles.homeIcon}
            >
              home
            </Icon>
            {/* <span style={styles.hideMenu} onClick={this.toggleHeader}>
              Hide Menu
            </span> */}
          </div>
        </div>
      );
    }
  };

  toggleHeader = () => {
    this.setState({ displayHeaders: !this.state.displayHeaders });
  };

  renderTopBar = () => {
    // if (!this.state.displayHeaders) return;
    const homeAppleTitleStyle =
      this.renderRouteName() === '' ? styles.headerTop : styles.headerTopSmall;
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
    // if (!this.state.displayHeaders)
    //   return (
    //     <span
    //       style={{
    //         color: 'gray',
    //         marginRight: '1em',
    //         cursor: 'pointer',
    //         fontSize: '10px',
    //         display: 'flex',
    //         justifyContent: 'flex-end',
    //       }}
    //       onClick={this.toggleHeader}
    //     >
    //       Show Menu
    //     </span>
    //   );

    return (
      <AppBar
        showMenuIconButton={false}
        titleStyle={styles.headerTitleBottom}
        style={styles.headerBottom}
        title={this.renderBottomBarTitle()}
      />
    );
  };

  openLineaWebSite = () => {
    window.open('http://www.linea.gov.br/', 'linea');
  };

  renderBottomBarTitle = () => {
    return (
      <div style={styles.bottom}>
        <span>
          © Copyright 2018, Powered by
          <a
            onClick={this.openLineaWebSite}
            title="LIneA"
            style={{ marginLeft: '8px' }}
          >
            <img src={logoLinea} alt={'logo linea'} style={styles.logoLinea} />
          </a>
        </span>
        <div style={styles.footerRight}>
          <span>
            {process.env.REACT_APP_VERSION ? process.env.REACT_APP_VERSION : ''}
          </span>
          {process.env.REACT_APP_OFFLINE === 'false' ? (
            this.state.websocketConnected ? (
              <Icon style={styles.connected}>check</Icon>
            ) : (
              <Icon style={styles.disconnected}>close</Icon>
            )
          ) : null}
        </div>
      </div>
    );
  };

  websocketConnected = () => {
    this.setState({ websocketConnected: true });
  };

  websocketDisconnected = () => {
    this.setState({ websocketConnected: false });
  };

  render() {
    const containerStyle = this.state.displayHeaders ? styles.container : null;
    const headerStyle =
      this.renderRouteName() === '' ? styles.headerContainer : null;
    const useGrid = this.renderRouteName() === '' ? null : styles.grid;
    return (
      <Provider store={store}>
        <ConnectedRouter history={history}>
          <MuiThemeProvider muiTheme={getMuiTheme(theme)}>
            <div style={useGrid}>
              <div style={headerStyle}>
                {this.renderRouteName() === '' ? (
                  <div style={styles.logoDesi}>
                    <img src={logo} alt={'logo'} style={styles.logo} />
                  </div>
                ) : null}
                {this.renderTopBar()}
              </div>
              <div style={containerStyle}>
                {['/', '/about', '/help', '/tutorials', '/contact'].map(
                  path => (
                    <Route
                      exact
                      key={path}
                      path={path}
                      render={() => <Landing updateUrl={this.updateUrl} />}
                    />
                  )
                )}
                {process.env.REACT_APP_OFFLINE === 'false' ? (
                  <OnlineContainer
                    connected={this.websocketConnected}
                    disconnected={this.websocketDisconnected}
                  />
                ) : null}
                <OfflineContainer toggleHeader={this.toggleHeader} />
              </div>
              <div style={styles.footerContainer}>{this.renderBottomBar()}</div>
            </div>
          </MuiThemeProvider>
        </ConnectedRouter>
      </Provider>
    );
  }
}

export default App;
