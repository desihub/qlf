import React from 'react';
import PropTypes from 'prop-types';
import { ArrowDropDown, ArrowDropUp } from 'material-ui-icons';
import { TableCell, TableHead, TableRow } from 'material-ui-next/Table';
import Checkbox from 'material-ui-next/Checkbox';
import Icon from 'material-ui-next/Icon';
import Popover from 'material-ui-next/Popover';
import QlfApi from '../../../../../containers/offline/connection/qlf-api';
import Radio, { RadioGroup } from 'material-ui-next/Radio';
import { FormControlLabel } from 'material-ui-next/Form';

const styles = {
  arrow: { display: 'flex', alignItems: 'center' },
  header: { cursor: 'pointer', color: 'black' },
  headerRecent: { color: 'black' },
  radioGroup: { margin: '1em' },
  tableCell: {
    padding: '4px 4px 4px 4px',
  },
};

export default class HistoryHeader extends React.Component {
  static muiName = 'TableHead';

  constructor(props) {
    super(props);
    this.state = {
      flavors: undefined,
      selectedFlavor: 'none',
    };
  }

  static propTypes = {
    type: PropTypes.string.isRequired,
    addOrder: PropTypes.func.isRequired,
    addFilters: PropTypes.func.isRequired,
    asc: PropTypes.bool,
    ordering: PropTypes.string,
    orderable: PropTypes.bool,
    selectable: PropTypes.bool,
    selectExposure: PropTypes.func,
  };

  componentWillMount() {
    if (this.props.orderable) this.getFlavors();
  }

  getFlavors = async () => {
    const flavors = await QlfApi.getFlavors();
    if (flavors && flavors.results) {
      this.setState({
        flavors: flavors.results.map(f => f.flavor),
      });
    }
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
    this.props.addOrder(id);
  };

  renderHeader = (id, name) => {
    const headerStyle = this.props.orderable
      ? styles.header
      : styles.headerRecent;
    return (
      <div style={styles.arrow}>
        <span style={headerStyle} onClick={() => this.fetchOrder(id)}>
          {name}
        </span>
        {this.props.orderable ? this.renderArrow(id) : null}
        {this.props.orderable ? this.renderFilter(id) : null}
        {this.props.orderable ? this.renderPopOver(id) : null}
      </div>
    );
  };

  renderFilter = filter => {
    if (filter === 'exposure__flavor' || filter === 'flavor') {
      return (
        <Icon
          onClick={event => this.handleFilterClick(event, filter)}
          style={{ fontSize: 20 }}
        >
          filter_list
        </Icon>
      );
    }
  };

  state = {
    anchorEl: null,
  };

  handleFilterClick = (event, filter) => {
    this.setState({
      anchorEl: event.currentTarget,
      filter,
    });
  };

  handlePopOverClose = () => {
    this.setState({
      anchorEl: null,
    });
  };

  renderPopOver = () => {
    return (
      <Popover
        open={Boolean(this.state.anchorEl)}
        anchorEl={this.state.anchorEl}
        onClose={this.handlePopOverClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'center',
        }}
        elevation={1}
      >
        {this.renderRadioGroup()}
      </Popover>
    );
  };

  renderRadioGroup = () => {
    return (
      <RadioGroup
        name="flavor"
        style={styles.radioGroup}
        value={this.state.selectedFlavor}
        onChange={this.handleRadioChange}
      >
        {this.state.flavors
          ? this.state.flavors.map(f => {
              return (
                <FormControlLabel
                  key={f}
                  value={`${this.state.filter}=${f}`}
                  control={<Radio />}
                  label={f}
                />
              );
            })
          : null}
        <FormControlLabel value="none" control={<Radio />} label="none" />
      </RadioGroup>
    );
  };

  handleRadioChange = evt => {
    const selectedFlavor = evt.target.value;
    this.setState({ selectedFlavor });
    if (selectedFlavor === 'none') {
      this.props.addFilters('');
    } else {
      this.props.addFilters(`${selectedFlavor}`);
    }
  };

  renderProcessingHistoryHeader = () => {
    return (
      <TableHead>
        <TableRow>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'Program')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('pk', 'Process ID')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure_id', 'Exp ID')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__tile', 'Tile ID')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('start', 'Process Date')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'Process Time')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__dateobs', 'OBS Date')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__dateobs', 'OBS Time')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'MJD')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__telra', 'RA (hms)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__teldec', 'Dec (dms)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__exptime', 'Exp Time(s)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__flavor', 'Flavor')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure__airmass', 'Airmass')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'FWHM (arcsec)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'QA')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'CCDs')}
          </TableCell>
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
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'Program')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exposure_id', 'Exp ID')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('tile', 'Tile ID')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('dateobs', 'OBS Date')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'OBS Time')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'MJD')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('telra', 'RA (hms)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('teldec', 'Dec (dms)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('exptime', 'Exp Time(s)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('flavor', 'Flavor')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'Airmass')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'FWHM (arcsec)')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'QA')}
          </TableCell>
          <TableCell style={styles.tableCell}>
            {this.renderHeader('', 'CCDs')}
          </TableCell>
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
