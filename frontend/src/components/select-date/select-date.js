import React from 'react';
import Proptypes from 'prop-types';
import TextField from '@material-ui/core/TextField';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'left',
  },
  spaceEnd: {
    paddingTop: '3vw',
  },
  label: {
    color: 'black',
  },
  dateField: {
    backgroundColor: 'white',
    border: '1px solid lightgrey',
    padding: 1,
  },
};

export default class SelectDate extends React.Component {
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
  };

  componentWillMount() {
    const startDate = new Date(this.props.startDate);
    const endDate = new Date(this.props.endDate);
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
    const startDate = new Date(nextProps.startDate);
    const endDate = new Date(nextProps.endDate);
    if (
      this.state.selectedStartDate !== startDate &&
      this.state.selectedEndDate !== endDate
    ) {
      this.setState({
        selectedStartDate: startDate,
        selectedEndDate: endDate,
      });
    }
  }

  changeStart = evt => {
    const selectedStartDate = new Date(evt.target.value);
    if (selectedStartDate.toString() !== 'Invalid Date')
      this.setState({ selectedStartDate }, this.selectRange);
  };

  changeEnd = evt => {
    const selectedEndDate = new Date(evt.target.value);
    if (selectedEndDate.toString() !== 'Invalid Date')
      this.setState({ selectedEndDate }, this.selectRange);
  };

  selectRange = () => {
    this.props.setHistoryRangeDate(
      this.formatFilterDate(this.state.selectedStartDate),
      this.formatFilterDate(this.state.selectedEndDate, true)
    );
  };

  formatFilterDate = (date, addOneDay) => {
    const month = (date.getMonth() + 1 < 10 ? '0' : '') + (date.getMonth() + 1);
    let day;
    if (addOneDay) {
      day = (date.getDate() + 1 < 10 ? '0' : '') + (date.getDate() + 1);
    } else {
      day = (date.getDate() + 1 < 10 ? '0' : '') + date.getDate();
    }
    return date.getFullYear() + '-' + month + '-' + day;
  };

  render() {
    return (
      <div style={styles.container}>
        <div>
          <TextField
            id="start"
            label="Start Date"
            type="date"
            value={this.formatFilterDate(this.state.selectedStartDate)}
            onChange={this.changeStart}
            InputLabelProps={{
              shrink: true,
            }}
            inputProps={{
              style: styles.dateField,
              // min: this.formatFilterDate(this.state.rangeStartDate),
              // max: this.formatFilterDate(this.state.selectedEndDate),
            }}
          />
        </div>
        <div style={styles.spaceEnd}>
          <TextField
            id="end"
            label="End Date"
            type="date"
            value={this.formatFilterDate(this.state.selectedEndDate)}
            onChange={this.changeEnd}
            InputLabelProps={{
              shrink: true,
            }}
            inputProps={{
              style: styles.dateField,
              // min: this.formatFilterDate(this.state.selectedStartDate, true),
              // max: this.formatFilterDate(this.state.rangeEndDate),
            }}
          />
        </div>
      </div>
    );
  }
}
