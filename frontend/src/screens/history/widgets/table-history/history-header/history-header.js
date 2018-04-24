import React from 'react';
import { TableHeaderColumn, TableRow, TableHeader } from 'material-ui/Table';
import PropTypes from 'prop-types';
import { ArrowDropDown, ArrowDropUp } from 'material-ui-icons';

const styles = {
  arrow: { display: 'flex', alignItems: 'center' },
  header: { cursor: 'pointer' },
};

export default class HistoryHeader extends React.Component {
  static muiName = 'TableHeader';
  static propTypes = {
    type: PropTypes.string.isRequired,
    getHistoryOrdered: PropTypes.func.isRequired,
    asc: PropTypes.bool,
    ordering: PropTypes.string,
  };

  renderArrow = id => {
    if (this.props.ordering === id) {
      if (this.props.asc) {
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
          onClick={() => this.props.getHistoryOrdered(id)}
        >
          {name}
        </span>
        {this.renderArrow(id)}
      </div>
    );
  };

  renderProcessingHistoryHeader = () => {
    return (
      <TableHeader
        displaySelectAll={false}
        adjustForCheckbox={false}
        enableSelectAll={false}
      >
        <TableRow>
          <TableHeaderColumn>Program</TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('pk', 'Process ID')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('start', 'Process Date')}
          </TableHeaderColumn>
          <TableHeaderColumn>Process Time</TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('exposure_id', 'Exp ID')}
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
    );
  };

  renderObservingHistoryHeader = () => {
    return (
      <TableHeader
        displaySelectAll={true}
        adjustForCheckbox={false}
        enableSelectAll={true}
        {...this.props}
      >
        <TableRow>
          <TableHeaderColumn>Program</TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('pk', 'Exp ID')}
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
    );
  };
  render() {
    return this.props.type === 'process'
      ? this.renderProcessingHistoryHeader()
      : this.renderObservingHistoryHeader();
  }
}
