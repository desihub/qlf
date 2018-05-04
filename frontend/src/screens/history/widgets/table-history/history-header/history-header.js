import React from 'react';
import PropTypes from 'prop-types';
import { ArrowDropDown, ArrowDropUp } from 'material-ui-icons';
import { TableCell, TableHead, TableRow } from 'material-ui-next/Table';
import Checkbox from 'material-ui-next/Checkbox';

const styles = {
  arrow: { display: 'flex', alignItems: 'center' },
  header: { cursor: 'pointer', color: 'black' },
};

export default class HistoryHeader extends React.Component {
  static muiName = 'TableHead';
  static propTypes = {
    type: PropTypes.string.isRequired,
    getHistory: PropTypes.func.isRequired,
    asc: PropTypes.bool,
    ordering: PropTypes.string,
    orderable: PropTypes.bool,
    selectable: PropTypes.bool,
    selectExposure: PropTypes.func,
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
    this.props.getHistory(id);
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
      <TableHead>
        <TableRow>
          <TableCell>{this.renderHeader('', 'Program')}</TableCell>
          <TableCell>{this.renderHeader('pk', 'Process ID')}</TableCell>
          <TableCell>{this.renderHeader('start', 'Process Date')}</TableCell>
          <TableCell>{this.renderHeader('', 'Process Time')}</TableCell>
          <TableCell>{this.renderHeader('exposure_id', 'Exp ID')}</TableCell>
          <TableCell>{this.renderHeader('tile', 'Tile ID')}</TableCell>
          <TableCell>{this.renderHeader('dateobs', 'OBS Date')}</TableCell>
          <TableCell>{this.renderHeader('', 'OBS Time')}</TableCell>
          <TableCell>{this.renderHeader('', 'MJD')}</TableCell>
          <TableCell>{this.renderHeader('telra', 'RA (hms)')}</TableCell>
          <TableCell>{this.renderHeader('teldec', 'Dec (dms)')}</TableCell>
          <TableCell>{this.renderHeader('exptime', 'Exp Time(s)')}</TableCell>
          <TableCell>{this.renderHeader('', 'Airmass')}</TableCell>
          <TableCell>{this.renderHeader('', 'FWHM (arcsec)')}</TableCell>
          <TableCell>{this.renderHeader('', 'QA')}</TableCell>
          <TableCell>{this.renderHeader('', 'View')}</TableCell>
        </TableRow>
      </TableHead>
    );
  };

  renderCheckbox = () => {
    if (!this.props.selectable) return;
    return (
      <TableCell padding="checkbox">
        <Checkbox
          onChange={(evt, checked) => this.props.selectExposure(checked)}
        />
      </TableCell>
    );
  };

  renderObservingHistoryHeader = () => {
    return (
      <TableHead>
        <TableRow>
          {this.renderCheckbox()}
          <TableCell>{this.renderHeader('', 'Program')}</TableCell>
          <TableCell>{this.renderHeader('exposure_id', 'Exp ID')}</TableCell>
          <TableCell>{this.renderHeader('tile', 'Tile ID')}</TableCell>
          <TableCell>{this.renderHeader('dateobs', 'OBS Date')}</TableCell>
          <TableCell>{this.renderHeader('', 'OBS Time')}</TableCell>
          <TableCell>{this.renderHeader('', 'MJD')}</TableCell>
          <TableCell>{this.renderHeader('telra', 'RA (hms)')}</TableCell>
          <TableCell>{this.renderHeader('teldec', 'Dec (dms)')}</TableCell>
          <TableCell>{this.renderHeader('exptime', 'Exp Time(s)')}</TableCell>
          <TableCell>{this.renderHeader('', 'Airmass')}</TableCell>
          <TableCell>{this.renderHeader('', 'FWHM (arcsec)')}</TableCell>
          <TableCell>{this.renderHeader('', 'QA')}</TableCell>
          <TableCell>{this.renderHeader('', 'View')}</TableCell>
        </TableRow>
      </TableHead>
    );
  };
  render() {
    return this.props.type === 'process'
      ? this.renderProcessingHistoryHeader()
      : this.renderObservingHistoryHeader();
  }
}
