import React from 'react';
import Proptypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import moment from 'moment';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'left',
  },
  space: {
    paddingLeft: '2vw',
  },
  label: {
    color: 'black',
  },
  dateField: {
    backgroundColor: 'white',
    border: '1px solid lightgrey',
    padding: 1,
    fontSize: '1.1vw',
    marginTop: '1vh',
    lineHeight: 1,
  },
  text: {
    fontSize: '1vw',
    paddingTop: '5px',
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
    if (addOneDay) {
      return moment(date)
        .add(1, 'days')
        .format('YYYY-MM-DD');
    } else {
      return moment(date).format('YYYY-MM-DD');
    }
  };

  render() {
    return (
      <div style={styles.container}>
        <div style={styles.space}>
          <TextField
            id="start"
            label="Start Date"
            type="date"
            defaultValue={this.formatFilterDate(this.state.rangeStartDate)}
            onChange={this.changeStart}
            InputLabelProps={{
              shrink: true,
              style: styles.text,
            }}
            inputProps={{
              style: styles.dateField,
              min: this.formatFilterDate(this.state.rangeStartDate),
              max: this.formatFilterDate(this.state.selectedEndDate),
            }}
          />
        </div>
        <div style={styles.space}>
          <TextField
            id="end"
            label="End Date"
            type="date"
            defaultValue={this.formatFilterDate(this.state.rangeEndDate)}
            onChange={this.changeEnd}
            InputLabelProps={{
              shrink: true,
              style: styles.text,
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
