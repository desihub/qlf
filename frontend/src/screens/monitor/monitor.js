import React, { Component } from 'react';
import Controls from './widgets/controls/controls';
import Stages from './widgets/stages/stages';
import Terminal from './widgets/terminal/terminal';
import Status from '../../components/status/status';
import PropTypes from 'prop-types';
import QA from '../qa/qa';
import ConfirmDialog from '../../components/dialog/dialog';

const styles = {
  topMenu: {
    marginRight: '1vw',
    marginLeft: '1vw',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '50% 50%',
    gridTemplateRows: 'auto 32vh',
    height: 'calc(100vh - 160px)',
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
    flexDirection: 'column',
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
    daemonRunning: PropTypes.bool.isRequired,
    pipelineRunning: PropTypes.string.isRequired,
    exposureId: PropTypes.string.isRequired,
    date: PropTypes.string,
    mainTerminal: PropTypes.array.isRequired,
    ingestionTerminal: PropTypes.array.isRequired,
    cameraTerminal: PropTypes.array.isRequired,
    camerasStages: PropTypes.object.isRequired,
    processId: PropTypes.string,
    qaTests: PropTypes.array,
    arms: PropTypes.array.isRequired,
    spectrographs: PropTypes.array.isRequired,
    time: PropTypes.string.isRequired,
    flavor: PropTypes.string.isRequired,
    mjd: PropTypes.string.isRequired,
    resetCameraLog: PropTypes.func.isRequired,
    navigateToCamera: PropTypes.func.isRequired,
  };

  state = {
    daemonRunning: false,
    pipelineRunning: 'Not Running',
    exposureId: '',
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
    arms: [],
    spectrographs: [],
    clearMonitor: false,
    processId: '',
    date: '',
    qaTests: [],
    confirmDialog: false,
    confirmDialogSubtitle: '',
  };

  componentDidMount() {
    document.title = 'Monitor';
  }

  componentWillReceiveProps(nextProps) {
    const {
      arms,
      cameraTerminal,
      camerasStages,
      pipelineRunning,
      date,
      exposureId,
      ingestionTerminal,
      mainTerminal,
      mjd,
      processId,
      qaTests,
      spectrographs,
      time,
      flavor,
    } = nextProps;

    this.setState({
      arms,
      cameraTerminal,
      camerasStages,
      pipelineRunning,
      date,
      exposureId,
      ingestionTerminal,
      mainTerminal,
      mjd,
      processId: processId,
      qaTests,
      spectrographs,
      time,
      flavor,
    });
  }

  openDialog = (cameraIndex, arm) => {
    this.props.navigateToCamera(arm, cameraIndex);
  };

  resetPipeline = () => {
    this.props.socketRef.state.ws.send('resetPipeline');
  };

  resetMonitor = () => {
    this.setState({
      confirmDialog: true,
      confirmDialogSubtitle: 'Are you sure you want to reset the screen?',
    });
  };

  closeConfirmDialog = () => {
    this.setState({ confirmDialog: false });
  };

  confirmReset = () => {
    this.resetPipeline();
  };

  render() {
    return (
      <div>
        <ConfirmDialog
          title={'Confirmation'}
          subtitle={this.state.confirmDialogSubtitle}
          open={this.state.confirmDialog}
          handleClose={this.closeConfirmDialog}
          onConfirm={this.confirmReset}
        />
        <div style={styles.topMenu}>
          <div style={styles.menu}>
            <Status
              exposureId={this.state.exposureId}
              pipelineRunning={this.state.pipelineRunning}
              layout={styles.layout}
              mjd={this.state.mjd}
              date={this.state.date}
              flavor={this.state.flavor}
              processId={String(this.state.processId)}
            />
            <Controls
              daemonRunning={this.props.daemonRunning}
              socket={this.props.socketRef}
              resetMonitor={this.resetMonitor}
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
              qaTests={this.state.qaTests}
              arms={this.state.arms}
              spectrographs={this.state.spectrographs}
              petalSizeFactor={22}
              monitor={true}
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
