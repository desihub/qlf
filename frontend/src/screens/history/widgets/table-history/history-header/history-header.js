import React from 'react';
import PropTypes from 'prop-types';
import { ArrowDropDown, ArrowDropUp } from 'material-ui-icons';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Checkbox from '@material-ui/core/Checkbox';
import Icon from '@material-ui/core/Icon';
import QlfApi from '../../../../../containers/offline/connection/qlf-api';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Popover from '@material-ui/core/Popover';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';

const styles = {
  header: { cursor: 'pointer', color: 'black' },
  headerRecent: { color: 'black' },
  radioGroup: { margin: '1em' },
  tableCell: {
    padding: '4px',
    textAlign: 'center',
  },
  itemText: {
    fontSize: '12px',
  },
  listIcon: { fontSize: 20, cursor: 'pointer', paddingRight: '8px' },
  listItem: { padding: '8px' },
};

export default class HistoryHeader extends React.Component {
  static muiName = 'TableHead';

  constructor(props) {
    super(props);
    this.state = {
      flavors: undefined,
      selectedFlavor: 'all',
      selectedStatus: 'all',
      id: undefined,
      anchorFilterEl: null,
      anchorEl: null,
    };
  }

  static propTypes = {
    type: PropTypes.string.isRequired,
    addOrder: PropTypes.func.isRequired,
    addFlavorFilter: PropTypes.func.isRequired,
    asc: PropTypes.bool,
    ordering: PropTypes.string,
    orderable: PropTypes.bool,
    selectable: PropTypes.bool,
    selectExposure: PropTypes.func,
    tableColumns: PropTypes.array.isRequired,
    openColumnsModal: PropTypes.func.isRequired,
    addStatusFilter: PropTypes.func.isRequired,
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

  fetchOrder = (id, asc) => {
    if (!id) return;
    this.handlePopOverClose();
    this.props.addOrder(id, asc);
  };

  renderHeader = (id, name) => {
    const headerStyle = this.props.orderable
      ? styles.header
      : styles.headerRecent;
    return (
      <div>
        <span
          style={headerStyle}
          onClick={event => this.handleHeaderClick(event, id)}
        >
          {name}
        </span>
        {this.props.orderable ? this.renderArrow(id) : null}
        {this.props.orderable ? this.renderPopOver(id) : null}
        {this.props.orderable ? this.renderFilterPopOver() : null}
      </div>
    );
  };

  handleHeaderClick = (event, id) => {
    this.setState({
      anchorEl: event.currentTarget,
      id,
    });
  };

  handlePopOverClose = () => {
    this.setState({
      anchorEl: null,
      anchorFilterEl: null,
    });
  };

  renderPopOver = () => {
    return (
      <Popover
        open={Boolean(this.state.anchorEl)}
        anchorEl={this.state.anchorEl}
        anchorOrigin={{ horizontal: 'left', vertical: 'bottom' }}
        transformOrigin={{ horizontal: 'left', vertical: 'top' }}
        onClose={this.handlePopOverClose}
        elevation={1}
      >
        <List component="nav">
          {this.state.id ? (
            <div>
              <ListItem
                onClick={() => this.fetchOrder(this.state.id, true)}
                style={styles.listItem}
                button
              >
                <Icon style={styles.listIcon}>arrow_upward</Icon>
                <span style={styles.itemText}>Sort Ascending</span>
              </ListItem>
              <Divider />
              <ListItem
                onClick={() => this.fetchOrder(this.state.id, false)}
                style={styles.listItem}
                button
              >
                <Icon style={styles.listIcon}>arrow_downward</Icon>
                <span style={styles.itemText}>Sort Descending</span>
              </ListItem>
              <Divider />
            </div>
          ) : null}
          {this.state.id &&
          (this.state.id.includes('flavor') ||
            this.state.id.includes('runtime')) ? (
            <div>
              <ListItem
                onClick={event => this.handleFilterClick(event, this.state.id)}
                style={styles.listItem}
                button
              >
                <Icon style={styles.listIcon}>filter_list</Icon>
                <span style={styles.itemText}>Filter</span>
              </ListItem>
              <Divider />
            </div>
          ) : null}
          <ListItem
            onClick={() => this.openColumnsModal()}
            style={styles.listItem}
            button
          >
            <Icon style={styles.listIcon}>view_column</Icon>
            <span style={styles.itemText}>Columns</span>
          </ListItem>
        </List>
      </Popover>
    );
  };

  handleFilterClick = (event, id) => {
    this.setState({
      anchorFilterEl: event.currentTarget,
      id,
    });
  };

  renderFilterPopOver = () => {
    return (
      <Popover
        open={Boolean(this.state.anchorFilterEl)}
        anchorEl={this.state.anchorFilterEl}
        anchorOrigin={{ horizontal: 'right', vertical: 'top' }}
        transformOrigin={{ horizontal: 'left', vertical: 'top' }}
        onClose={this.handlePopOverClose}
        elevation={1}
      >
        {this.state.id === 'runtime'
          ? this.renderStatusRadioGroup()
          : this.renderFlavorRadioGroup()}
      </Popover>
    );
  };

  openColumnsModal = () => {
    this.handlePopOverClose();
    this.props.openColumnsModal();
  };

  handleStatusRadioChange = evt => {
    const selectedStatus = evt.target.value;
    this.setState({ selectedStatus });
    this.props.addStatusFilter(selectedStatus);
    this.handlePopOverClose();
  };

  renderStatusRadioGroup = () => {
    return (
      <RadioGroup
        name="flavor"
        style={styles.radioGroup}
        value={this.state.selectedStatus}
        onChange={this.handleStatusRadioChange}
      >
        <FormControlLabel value="abort" control={<Radio />} label="Abort" />
        <FormControlLabel value="fail" control={<Radio />} label="Fail" />
        <FormControlLabel value="normal" control={<Radio />} label="Normal" />
        <FormControlLabel value="all" control={<Radio />} label="All" />
      </RadioGroup>
    );
  };

  handleFlavorRadioChange = evt => {
    const selectedFlavor = evt.target.value;
    const filterName =
      this.props.type === 'process' ? 'exposure__flavor' : 'flavor';
    this.setState({ selectedFlavor });
    if (selectedFlavor === 'all') {
      this.props.addFlavorFilter(`${filterName}=`);
    } else {
      this.props.addFlavorFilter(`${filterName}=${selectedFlavor}`);
    }
    this.handlePopOverClose();
  };

  renderFlavorRadioGroup = () => {
    return (
      <RadioGroup
        name="flavor"
        style={styles.radioGroup}
        value={this.state.selectedFlavor}
        onChange={this.handleFlavorRadioChange}
      >
        {this.state.flavors
          ? this.state.flavors.map(f => {
              return (
                <FormControlLabel
                  key={f}
                  value={f}
                  control={<Radio />}
                  label={f}
                />
              );
            })
          : null}
        <FormControlLabel value="all" control={<Radio />} label="All" />
      </RadioGroup>
    );
  };

  renderProcessingHistoryHeader = () => {
    return (
      <TableHead>
        <TableRow>
          {this.props.tableColumns.map((column, id) => {
            return (
              <TableCell key={`PROCESS${id}`} style={styles.tableCell}>
                {this.renderHeader(column.key, column.name)}
              </TableCell>
            );
          })}
        </TableRow>
      </TableHead>
    );
  };

  renderCheckbox = () => {
    if (!this.props.selectable) return;
    return (
      <TableCell style={styles.tableCell}>
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
          {process.env.REACT_APP_OFFLINE === 'true'
            ? null
            : this.renderCheckbox()}
          {this.props.tableColumns
            .filter(column => column.key !== null)
            .map((column, id) => {
              return (
                <TableCell key={`EXP${id}`} style={styles.tableCell}>
                  {this.renderHeader(column.key, column.name)}
                </TableCell>
              );
            })}
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
