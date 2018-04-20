import React, { Component } from 'react';
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';
import { ArrowDropDown, ArrowDropUp } from 'material-ui-icons';
import Proptypes from 'prop-types';
import { Card } from 'material-ui/Card';

const styles = {
  arrow: { display: 'flex', alignItems: 'center' },
  header: { cursor: 'pointer' },
  card: {
    borderLeft: 'solid 4px teal',
    flex: '1',
    height: '90%',
    margin: '1em',
  },
  link: {
    cursor: 'pointer',
    textDecoration: 'none',
  },
  bold: { fontWeight: 900 },
};

export default class TableHistory extends Component {
  static propTypes = {
    getHistory: Proptypes.func.isRequired,
    getHistoryOrdered: Proptypes.func.isRequired,
    rows: Proptypes.array.isRequired,
    navigateToQA: Proptypes.func.isRequired,
    lastProcess: Proptypes.number,
    type: Proptypes.string.isRequired,
  };

  state = {
    rows: undefined,
    asc: undefined,
    ordering: undefined,
  };

  componentWillMount() {
    this.props.getHistory();
  }

  getHistoryOrdered = async ordering => {
    const order = this.state.asc ? ordering : `-${ordering}`;
    this.setState({
      rows: await this.props.getHistoryOrdered(order),
      asc: !this.state.asc,
      ordering,
    });
  };

  selectProcessQA = pk => {
    this.props.navigateToQA(pk);
  };

  renderBody = () => {
    return (
      <TableBody showRowHover={true} displayRowCheckbox={false}>
        {this.props.rows.map((process, id) => {
          const lastProcessStyle =
            process.pk === this.props.lastProcess ? styles.bold : null;
          const processId = this.props.type === 'process' ? process.pk : process.last_exposure_process_id;
          return (
            <TableRow style={lastProcessStyle} key={id}>
              <TableRowColumn />
              {this.props.type === 'process' ? (
                <TableRowColumn>{process.pk}</TableRowColumn>
              ) : null}
              {this.props.type === 'process' ? (
                <TableRowColumn>
                  {this.formatDate(process.start)}
                </TableRowColumn>
              ) : null}
              {this.props.type === 'process' ? (
                <TableRowColumn>{process.runtime}</TableRowColumn>
              ) : null}
              <TableRowColumn>
                {this.props.type === 'process'
                  ? process.exposure_id
                  : process.pk}
              </TableRowColumn>
              <TableRowColumn>{process.tile}</TableRowColumn>
              <TableRowColumn>
                {this.formatDate(process.dateobs)}
              </TableRowColumn>
              <TableRowColumn>
                {this.formatTime(process.dateobs)}
              </TableRowColumn>
              <TableRowColumn>{process.datemjd.toFixed(2)}</TableRowColumn>
              <TableRowColumn>{process.telra}</TableRowColumn>
              <TableRowColumn>{process.teldec}</TableRowColumn>
              <TableRowColumn>{process.exptime}</TableRowColumn>
              <TableRowColumn>{process.airmass}</TableRowColumn>
              <TableRowColumn />
              <TableRowColumn>
                <span
                  style={styles.link}
                  onClick={() => this.selectProcessQA(processId)}
                >
                  View
                </span>
              </TableRowColumn>
              <TableRowColumn />
            </TableRow>
          );
        })}
      </TableBody>
    );
  };

  renderArrow = id => {
    if (this.state.ordering === id) {
      if (this.state.asc) {
        return <ArrowDropUp />;
      } else {
        return <ArrowDropDown />;
      }
    }
  };

  renderHeader = (id, name) => {
    return (
      <div style={styles.arrow}>
        <span style={styles.header} onClick={() => this.getHistoryOrdered(id)}>
          {name}
        </span>
        {this.renderArrow(id)}
      </div>
    );
  };

  formatDate = dateString => {
    const date = new Date(dateString);
    const month = (date.getMonth() + 1 < 10 ? '0' : '') + (date.getMonth() + 1);
    const day = (date.getDate() + 1 < 10 ? '0' : '') + date.getDate();
    return month + '/' + day + '/' + date.getFullYear();
  };

  formatTime = dateString => {
    const time = new Date(dateString);
    const hour = (time.getHours() + 1 < 10 ? '0' : '') + time.getHours();
    const minutes = (time.getMinutes() + 1 < 10 ? '0' : '') + time.getMinutes();
    const seconds = (time.getSeconds() + 1 < 10 ? '0' : '') + time.getDate();
    return hour + ':' + minutes + ':' + seconds;
  };

  render() {
    return (
      <Card style={styles.card}>
        <Table
          fixedHeader={false}
          style={{ width: 'auto', tableLayout: 'auto' }}
          bodyStyle={{ overflow: 'visible' }}
        >
          <TableHeader
            displaySelectAll={false}
            adjustForCheckbox={false}
            enableSelectAll={false}
          >
            <TableRow>
              <TableHeaderColumn>Program</TableHeaderColumn>
              {this.props.type === 'process' ? (
                <TableHeaderColumn>
                  {this.renderHeader('pk', 'Process ID')}
                </TableHeaderColumn>
              ) : null}
              {this.props.type === 'process' ? (
                <TableHeaderColumn>
                  {this.renderHeader('start', 'Process Date')}
                </TableHeaderColumn>
              ) : null}
              {this.props.type === 'process' ? (
                <TableHeaderColumn>Process Time</TableHeaderColumn>
              ) : null}
              <TableHeaderColumn>
                {this.renderHeader(
                  this.props.type === 'process' ? 'exposure_id' : 'pk',
                  'Exp ID'
                )}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('tile', 'Tile ID')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('dateobs', 'OBS Date')}
              </TableHeaderColumn>
              <TableHeaderColumn>OBS Time</TableHeaderColumn>
              <TableHeaderColumn>MJD</TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('telra', 'RA (hms)')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('teldec', 'Dec (dms)')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('exptime', 'Exp Time(s)')}
              </TableHeaderColumn>
              <TableHeaderColumn>Airmass</TableHeaderColumn>
              <TableHeaderColumn>FWHM (arcsec)</TableHeaderColumn>
              <TableHeaderColumn>QA</TableHeaderColumn>
              <TableHeaderColumn>View</TableHeaderColumn>
            </TableRow>
          </TableHeader>
          {this.renderBody()}
        </Table>
      </Card>
    );
  }
}
