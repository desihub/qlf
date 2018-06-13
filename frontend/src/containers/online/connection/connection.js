import React from 'react';
import PropTypes from 'prop-types';

class Websocket extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ws: new WebSocket(this.props.url, this.props.protocol),
      attempts: 1,
    };
  }

  generateInterval(k) {
    if (this.props.reconnectIntervalInMilliSeconds > 0) {
      return this.props.reconnectIntervalInMilliSeconds;
    }
    return Math.min(30, Math.pow(2, k) - 1) * 1000;
  }

  setupWebsocket() {
    const websocket = this.state.ws;

    websocket.onopen = () => {
      if (typeof this.props.onOpen === 'function') this.props.onOpen();
    };

    websocket.onmessage = evt => {
      this.props.onMessage(evt.data);
    };

    this.shouldReconnect = this.props.reconnect;
    websocket.onclose = () => {
      if (typeof this.props.onClose === 'function') this.props.onClose();
      if (this.shouldReconnect) {
        const time = this.generateInterval(this.state.attempts);
        this.timeoutID = setTimeout(() => {
          this.setState({ attempts: this.state.attempts + 1 });
          this.setState({
            ws: new WebSocket(this.props.url, this.props.protocol),
          });
          this.setupWebsocket();
        }, time);
      }
    };
  }

  componentDidMount() {
    this.setupWebsocket();
  }

  componentWillUnmount() {
    this.shouldReconnect = false;
    clearTimeout(this.timeoutID);
    const websocket = this.state.ws;
    websocket.close();
  }

  sendMessage(message) {
    const websocket = this.state.ws;
    websocket.send(message);
  }

  render() {
    return <div />;
  }
}

Websocket.defaultProps = {
  debug: false,
  reconnect: true,
};

Websocket.propTypes = {
  url: PropTypes.string.isRequired,
  onMessage: PropTypes.func.isRequired,
  onOpen: PropTypes.func,
  onClose: PropTypes.func,
  debug: PropTypes.bool,
  reconnect: PropTypes.bool,
  protocol: PropTypes.string,
  reconnectIntervalInMilliSeconds: PropTypes.number,
};

export default Websocket;
