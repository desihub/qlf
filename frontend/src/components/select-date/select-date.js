import React from 'react';
import Proptypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import moment from 'moment';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  rowContainer: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'left',
  },
  rowSpace: {
    paddingLeft: '2vw',
  },
  columnContainer: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'left',
  },
  columnSpace: {
    paddingBottom: '2.5vh',
  },
  label: {
    color: 'black',
  },
  dateField: {
    backgroundColor: 'white',
    border: '1px solid lightgrey',
    padding: 1,
    fontSize: '0.92vw',
    marginTop: '1.05vh',
    lineHeight: '2vh',
  },
  title: {
    fontSize: '1.2vw',
  },
  field: {
    minWidth: '100%',
  },
};

class SelectDate extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      rangeStartDate: undefined,
      rangeEndDate: undefined,
      selectedStartDate: undefined,
      selectedEndDate: undefined,
    };
  }

  static propTypes = {
    startDate: Proptypes.string.isRequired,
    endDate: Proptypes.string.isRequired,
    setHistoryRangeDate: Proptypes.func.isRequired,
    row: Proptypes.bool,
    classes: Proptypes.object.isRequired,
  };

  componentWillMount() {
    const startDate = moment(this.props.startDate).format('YYYY-MM-DD');
    const endDate = moment(this.props.endDate).format('YYYY-MM-DD');
    if (
      this.state.rangeStartDate !== startDate &&
      this.state.rangeEndDate !== endDate
    ) {
      this.setState({
        rangeStartDate: startDate,
        rangeEndDate: endDate,
        selectedStartDate: startDate,
        selectedEndDate: endDate,
      });
    }
  }

  componentWillReceiveProps(nextProps) {
    const startDate = moment(nextProps.startDate).format('YYYY-MM-DD');
    const endDate = moment(nextProps.endDate).format('YYYY-MM-DD');
    if (
      !nextProps.row &&
      (this.state.selectedStartDate !== startDate ||
        this.state.selectedEndDate !== endDate)
    ) {
      this.setState({
        selectedStartDate: startDate,
        selectedEndDate: endDate,
      });
    }
  }

  changeStart = evt => {
    const selectedStartDate = moment(evt.target.value).format('YYYY-MM-DD');
    if (selectedStartDate.toString() !== 'Invalid Date')
      this.setState({ selectedStartDate }, this.selectRange);
  };

  changeEnd = evt => {
    const selectedEndDate = moment(evt.target.value).format('YYYY-MM-DD');
    if (selectedEndDate.toString() !== 'Invalid Date')
      this.setState({ selectedEndDate }, this.selectRange);
  };

  selectRange = () => {
    this.props.setHistoryRangeDate(
      this.formatFilterDate(this.state.selectedStartDate),
      this.formatFilterDate(this.state.selectedEndDate)
    );
  };

  formatFilterDate = (date, addOneDay) => {
    if (addOneDay) {
      return moment(date)
        .add(1, 'days')
        .format('YYYY-MM-DD');
    } else {
      return moment(date).format('YYYY-MM-DD');
    }
  };

  render() {
    const containerStyle = this.props.row
      ? styles.rowContainer
      : styles.columnContainer;
    const spaceStyle = this.props.row ? styles.rowSpace : styles.columnSpace;
    return (
      <div style={containerStyle}>
        <div style={spaceStyle}>
          <TextField
            id="start"
            label="Start Date"
            type="date"
            value={this.formatFilterDate(this.state.selectedStartDate)}
            onChange={this.changeStart}
            style={styles.field}
            InputLabelProps={{
              shrink: true,
              style: styles.title,
            }}
            inputProps={{
              style: styles.dateField,
              min: this.formatFilterDate(this.state.rangeStartDate),
              max: this.formatFilterDate(this.state.selectedEndDate),
            }}
          />
        </div>
        <div style={spaceStyle}>
          <TextField
            id="end"
            label="End Date"
            type="date"
            value={this.formatFilterDate(this.state.selectedEndDate)}
            onChange={this.changeEnd}
            style={styles.field}
            InputLabelProps={{
              shrink: true,
              style: styles.title,
            }}
            inputProps={{
              style: styles.dateField,
              min: this.formatFilterDate(this.state.selectedStartDate, true),
              max: this.formatFilterDate(this.state.rangeEndDate),
            }}
          />
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(SelectDate);
