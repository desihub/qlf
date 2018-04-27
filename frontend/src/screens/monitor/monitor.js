import React, { Component } from 'react';
import Controls from './widgets/controls/controls';
import Stages from './widgets/stages/stages';
import Terminal from './widgets/terminal/terminal';
import Status from '../../components/status/status';
import Dialog from './widgets/dialog/dialog';
import PropTypes from 'prop-types';
import QA from '../qa/qa';

const styles = {
  topMenu: {
    marginTop: '1vh',
    marginRight: '1vw',
    marginLeft: '1vw',
  },
  grid: {
    flex: 1,
    display: 'grid',
    marginBottom: '1vh',
    flexDirection: 'row',
    gridTemplateColumns: '50% 50%',
    gridTemplateRows: 'auto 32vh',
  },
  gridItem: {
    paddingTop: '1vh',
    paddingLeft: '1vw',
    paddingRight: '1vw',
    display: 'flex',
    justifyContent: 'left',
    alignItems: 'center',
  },
  menu: {
    flex: 1,
    display: 'flex',
    marginBottom: '1vh',
    flexDirection: 'row',
    gridTemplateColumns: 'auto auto',
  },
  column: {
    flexDirection: 'column',
    padding: '0vh 1vw',
    display: 'flex',
    justifyContent: 'space-between',
    paddingBottom: '1vh',
  },
};

export default class Monitor extends Component {
  static propTypes = {
    socketRef: PropTypes.object,
    daemonStatus: PropTypes.string.isRequired,
    exposure: PropTypes.string.isRequired,
    date: PropTypes.string,
    mainTerminal: PropTypes.array.isRequired,
    ingestionTerminal: PropTypes.array.isRequired,
    cameraTerminal: PropTypes.array.isRequired,
    camerasStages: PropTypes.object.isRequired,
    processId: PropTypes.number,
    qaTests: PropTypes.array.isRequired,
    arms: PropTypes.array.isRequired,
    spectrographs: PropTypes.array.isRequired,
  };

  state = {
    daemonStatus: 'idle',
    exposure: 'none',
    width: '0',
    height: '0',
    openDialog: false,
    cameraIndex: 0,
    mainTerminal: [],
    ingestionTerminal: [],
    cameraTerminal: [],
    layout: {},
    camerasStages: { b: [], r: [], z: [] },
    mjd: '',
  };

  componentWillReceiveProps(nextProps) {
    this.setState({ ...nextProps });
  }

  openDialog = (cameraIndex, arm) => {
    this.props.socketRef.state.ws.send(`camera:${arm}${cameraIndex}`);
    this.setState({ cameraIndex, openDialog: true });
  };

  closeDialog = () => {
    this.setState({ openDialog: false });
  };

  render() {
    return (
      <div>
        <Dialog
          lines={this.state.cameraTerminal}
          openDialog={this.state.openDialog}
          cameraIndex={this.state.cameraIndex}
          closeDialog={this.closeDialog}
        />
        <div style={styles.topMenu}>
          <div style={styles.menu}>
            <Controls
              daemonStatus={this.props.daemonStatus}
              socket={this.props.socketRef}
            />
            <Status
              exposure={this.state.exposure}
              daemonStatus={this.state.daemonStatus}
              layout={styles.layout}
              mjd={this.state.mjd}
              date={this.props.date}
              processId={this.props.processId}
            />
          </div>
        </div>
        <div style={styles.grid}>
          <div style={styles.column}>
            <Stages
              status={this.state.camerasStages.b}
              arm={'b'}
              openDialog={this.openDialog}
              renderHeader={true}
            />
            <Stages
              status={this.state.camerasStages.r}
              arm={'r'}
              openDialog={this.openDialog}
              renderHeader={false}
            />
            <Stages
              status={this.state.camerasStages.z}
              arm={'z'}
              openDialog={this.openDialog}
              renderHeader={false}
            />
          </div>
          <div style={styles.gridItem}>
            <QA
              qaTests={this.props.qaTests}
              arms={this.props.arms}
              spectrographs={this.props.spectrographs}
              petalSizeFactor={22}
            />
          </div>
          <div style={styles.gridItem}>
            <Terminal height={'100%'} lines={this.state.ingestionTerminal} />
          </div>
          <div style={styles.gridItem}>
            ￼ <Terminal height={'100%'} lines={this.state.mainTerminal} />
          </div>
        </div>
      </div>
    );
  }
}
