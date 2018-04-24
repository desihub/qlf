import React, { Component } from 'react';
import Controls from './widgets/controls/controls';
import Stages from './widgets/stages/stages';
import Terminal from './widgets/terminal/terminal';
import Status from '../../components/status/status';
import Dialog from './widgets/dialog/dialog';
import PropTypes from 'prop-types';
import QA from '../qa/qa';

const styles = {
  topMenu: { marginTop: '1vh', marginRight: '1vw', marginLeft: '1vw' },
  leftCol: { flex: 1, marginRight: '1vw', marginLeft: '1vw' },
  rightCol: { flex: 1, marginLeft: '1vw', marginRight: '1vw' },
  singleCol: { marginBottom: '1vh' },
};

export default class Monitor extends Component {
  constructor(props) {
    super(props);
    this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
  }

  static propTypes = {
    socketRef: PropTypes.object,
    daemonStatus: PropTypes.string.isRequired,
    exposure: PropTypes.string.isRequired,
    date: PropTypes.string,
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
    ingestionTerminal: [],
    cameraTerminal: [],
    layout: {},
    camerasStages: { b: [], r: [], z: [] },
    mjd: '',
  };

  componentDidMount() {
    this.updateWindowDimensions();
    window.addEventListener('resize', this.updateWindowDimensions);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ ...nextProps });
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updateWindowDimensions);
  }

  updateWindowDimensions() {
    this.setState({
      layout: {
        flex: 1,
        display: 'flex',
        marginBottom: '1vh',
        flexDirection: window.innerWidth < 800 ? 'row' : 'row',
      },
    });
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
          <div style={this.state.layout}>
            <Controls
              daemonStatus={this.props.daemonStatus}
              socket={this.props.socketRef}
            />
            <Status
              exposure={this.state.exposure}
              daemonStatus={this.state.daemonStatus}
              layout={this.state.layout}
              mjd={this.state.mjd}
              date={this.props.date}
              processId={this.props.processId}
            />
          </div>
        </div>
        <div style={this.state.layout}>
          <div style={styles.leftCol}>
            <div style={this.state.layout}>
              <Stages
                status={this.state.camerasStages.b}
                arm={'b'}
                openDialog={this.openDialog}
                renderHeader={true}
              />
            </div>
            <div style={this.state.layout}>
              <Stages
                status={this.state.camerasStages.r}
                arm={'r'}
                openDialog={this.openDialog}
                renderHeader={false}
              />
            </div>
            <div style={this.state.layout}>
              <Stages
                status={this.state.camerasStages.z}
                arm={'z'}
                openDialog={this.openDialog}
                renderHeader={false}
              />
            </div>
            <div style={styles.singleCol}>
              <Terminal height={'37vh'} lines={this.state.ingestionTerminal} />
            </div>
          </div>
          <div style={styles.rightCol}>
            <QA
              qaTests={this.props.qaTests}
              arms={this.props.arms}
              spectrographs={this.props.spectrographs}
              petalSizeFactor={20}
            />
          </div>
        </div>
      </div>
    );
  }
}
