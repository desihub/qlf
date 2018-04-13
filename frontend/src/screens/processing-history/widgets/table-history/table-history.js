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
};

export default class TableHistory extends Component {
  static propTypes = {
    getProcessingHistory: Proptypes.func.isRequired,
    getProcessingHistoryOrdered: Proptypes.func.isRequired,
    processes: Proptypes.array.isRequired,
    navigateToQA: Proptypes.func.isRequired,
  };

  state = {
    processes: undefined,
    asc: undefined,
    ordering: undefined,
  };

  componentWillMount() {
    this.props.getProcessingHistory();
  }

  getProcessingHistoryOrdered = async ordering => {
    const order = this.state.asc ? ordering : `-${ordering}`;
    this.setState({
      processes: await this.props.getProcessingHistoryOrdered(order),
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
        {this.props.processes.map((process, id) => {
          return (
            <TableRow key={id}>
              <TableRowColumn>{process.pk}</TableRowColumn>
              <TableRowColumn>{process.dateobs}</TableRowColumn>
              <TableRowColumn>{process.datemjd.toFixed(5)}</TableRowColumn>
              <TableRowColumn>{process.exposure_id}</TableRowColumn>
              <TableRowColumn>{process.tile}</TableRowColumn>
              <TableRowColumn>{process.telra}</TableRowColumn>
              <TableRowColumn>{process.teldec}</TableRowColumn>
              <TableRowColumn />
              <TableRowColumn>{process.exptime}</TableRowColumn>
              <TableRowColumn>{process.airmass}</TableRowColumn>
              <TableRowColumn />
              <TableRowColumn>{process.runtime}</TableRowColumn>
              <TableRowColumn>
                <span
                  style={styles.link}
                  onClick={() => this.selectProcessQA(process.pk)}
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
        <span
          style={styles.header}
          onClick={() => this.getProcessingHistoryOrdered(id)}
        >
          {name}
        </span>
        {this.renderArrow(id)}
      </div>
    );
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
              <TableHeaderColumn>
                {this.renderHeader('pk', 'Process ID')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('dateobs', 'Date OBS')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('datemjd', 'MJD')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('exposure_id', 'Exp ID')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('tile', 'Tile ID')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('telra', 'RA (hms)')}
              </TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('teldec', 'Dec (dms)')}
              </TableHeaderColumn>
              <TableHeaderColumn>Program</TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('exptime', 'Exp Time(s)')}
              </TableHeaderColumn>
              <TableHeaderColumn>Airmass</TableHeaderColumn>
              <TableHeaderColumn>FWHM (arcsec)</TableHeaderColumn>
              <TableHeaderColumn>
                {this.renderHeader('runtime', 'Run time')}
              </TableHeaderColumn>
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
