import React from 'react';
import { TableHeaderColumn, TableRow, TableHeader } from 'material-ui/Table';
import PropTypes from 'prop-types';
import { ArrowDropDown, ArrowDropUp } from 'material-ui-icons';

const styles = {
  arrow: { display: 'flex', alignItems: 'center' },
  header: { cursor: 'pointer', color: 'black' },
};

export default class HistoryHeader extends React.Component {
  static muiName = 'TableHeader';
  static propTypes = {
    type: PropTypes.string.isRequired,
    getHistoryOrdered: PropTypes.func.isRequired,
    asc: PropTypes.bool,
    ordering: PropTypes.string,
    orderable: PropTypes.bool,
    selectable: PropTypes.bool,
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

  fetchOrder = id => {
    if (!id) return;
    this.props.getHistoryOrdered(id);
  };

  renderHeader = (id, name) => {
    return (
      <div style={styles.arrow}>
        <span style={styles.header} onClick={() => this.fetchOrder(id)}>
          {name}
        </span>
        {this.props.orderable ? this.renderArrow(id) : null}
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
          <TableHeaderColumn>
            {this.renderHeader('', 'Program')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('pk', 'Process ID')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('start', 'Process Date')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('', 'Process Time')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('exposure_id', 'Exp ID')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('tile', 'Tile ID')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('dateobs', 'OBS Date')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('', 'OBS Time')}
          </TableHeaderColumn>
          <TableHeaderColumn>{this.renderHeader('', 'MJD')}</TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('telra', 'RA (hms)')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('teldec', 'Dec (dms)')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('exptime', 'Exp Time(s)')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('', 'Airmass')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('', 'FWHM (arcsec)')}
          </TableHeaderColumn>
          <TableHeaderColumn>{this.renderHeader('', 'QA')}</TableHeaderColumn>
          <TableHeaderColumn>{this.renderHeader('', 'View')}</TableHeaderColumn>
        </TableRow>
      </TableHeader>
    );
  };

  renderObservingHistoryHeader = () => {
    return (
      <TableHeader
        displaySelectAll={true && this.props.selectable}
        adjustForCheckbox={false}
        enableSelectAll={true && this.props.selectable}
        {...this.props}
      >
        <TableRow>
          <TableHeaderColumn>
            {this.renderHeader('', 'Program')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('exposure_id', 'Exp ID')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('tile', 'Tile ID')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('dateobs', 'OBS Date')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('', 'OBS Time')}
          </TableHeaderColumn>
          <TableHeaderColumn>{this.renderHeader('', 'MJD')}</TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('telra', 'RA (hms)')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('teldec', 'Dec (dms)')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('exptime', 'Exp Time(s)')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('', 'Airmass')}
          </TableHeaderColumn>
          <TableHeaderColumn>
            {this.renderHeader('', 'FWHM (arcsec)')}
          </TableHeaderColumn>
          <TableHeaderColumn>{this.renderHeader('', 'QA')}</TableHeaderColumn>
          <TableHeaderColumn>{this.renderHeader('', 'View')}</TableHeaderColumn>
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
