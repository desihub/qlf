import React from 'react';
import Proptypes from 'prop-types';
import TextField from '@material-ui/core/TextField';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'left',
  },
  space: {
    paddingBottom: '2.5vh',
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
    selectedStartDate: Proptypes.string.isRequired,
    selectedEndDate: Proptypes.string.isRequired,
    setHistoryRangeDate: Proptypes.func.isRequired,
  };

  componentWillMount() {
    const { startDate, endDate } = this.props;
    if (
      this.state.rangeStartDate !== startDate &&
      this.state.rangeEndDate !== endDate
    ) {
      this.setState({
        rangeStartDate: startDate.split('T')[0],
        rangeEndDate: endDate.split('T')[0],
        selectedStartDate: startDate.split('T')[0],
        selectedEndDate: endDate.split('T')[0],
      });
    }
    const { selectedStartDate, selectedEndDate } = this.props;
    if (
      selectedStartDate.toString() !== 'Invalid Date' &&
      selectedEndDate.toString() !== 'Invalid Date' &&
      this.state.selectedStartDate !== selectedStartDate &&
      this.state.selectedEndDate !== selectedEndDate
    ) {
      this.setState({
        selectedStartDate: selectedStartDate.split('T')[0],
        selectedEndDate: selectedEndDate.split('T')[0],
      });
    }
  }

  changeStart = evt => {
    const selectedStartDate = evt.target.value;
    this.setState({ selectedStartDate }, this.selectRange);
  };

  changeEnd = evt => {
    const selectedEndDate = evt.target.value;
    this.setState({ selectedEndDate }, this.selectRange);
  };

  selectRange = () => {
    this.props.setHistoryRangeDate(
      this.formatFilterDate(this.state.selectedStartDate),
      this.formatFilterDate(this.state.selectedEndDate)
    );
  };

  formatFilterDate = dateString => {
    const date = new Date(dateString);
    const month = (date.getMonth() + 1 < 10 ? '0' : '') + (date.getMonth() + 1);
    const day = (date.getDate() + 1 < 10 ? '0' : '') + (date.getDate() + 1);
    return date.getFullYear() + '-' + month + '-' + day;
  };

  render() {
    const {
      selectedStartDate,
      selectedEndDate,
      rangeStartDate,
      rangeEndDate,
    } = this.state;
    const selectedStart = selectedStartDate !== '';
    const selectedEnd = selectedEndDate !== '';
    const defaultStart = selectedStart ? selectedStartDate : rangeStartDate;
    const defaultEnd = selectedEnd ? selectedEndDate : rangeEndDate;
    return (
      <div style={styles.container}>
        <div style={styles.space}>
          <TextField
            id="start"
            label="Start Date"
            type="date"
            defaultValue={this.formatFilterDate(defaultStart)}
            onChange={this.changeStart}
            InputLabelProps={{
              shrink: true,
            }}
            inputProps={{
              style: styles.dateField,
              min: this.formatFilterDate(rangeStartDate),
              max: this.formatFilterDate(defaultEnd),
            }}
          />
        </div>
        <div style={styles.space}>
          <TextField
            id="end"
            label="End Date"
            type="date"
            defaultValue={this.formatFilterDate(defaultEnd)}
            onChange={this.changeEnd}
            InputLabelProps={{
              shrink: true,
            }}
            inputProps={{
              style: styles.dateField,
              min: this.formatFilterDate(defaultStart),
              max: this.formatFilterDate(rangeEndDate),
            }}
          />
        </div>
      </div>
    );
  }
}
