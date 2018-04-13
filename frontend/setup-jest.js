global.fetch = require('jest-fetch-mock'); // eslint-disable-line

process.env.REACT_APP_API = 'http://localhost:8001/';
process.env.REACT_APP_WEBSOCKET = 'ws://localhost:8000';
process.env.REACT_APP_BOKEH = 'http://localhost:8001/dashboard/';
