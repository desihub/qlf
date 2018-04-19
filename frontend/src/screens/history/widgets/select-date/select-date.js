import React from 'react';
import DatePicker from 'material-ui/DatePicker';
import Proptypes from 'prop-types';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'center',
  },
  space: {
    marginRight: '2vw',
  },
};

export default class SelectDate extends React.Component {
  static propTypes = {
    startDate: Proptypes.string.isRequired,
    endDate: Proptypes.string.isRequired,
    getHistoryRangeDate: Proptypes.func.isRequired,
  };

  state = {
    rangeStartDate: undefined,
    rangeEndDate: undefined,
    selectedStartDate: undefined,
    selectedEndDate: undefined,
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

  changeStart = (evt, selectedStartDate) => {
    this.setState({ selectedStartDate }, this.selectRange);
  };

  changeEnd = (evt, selectedEndDate) => {
    this.setState({ selectedEndDate }, this.selectRange);
  };

  selectRange = () => {
    this.props.getHistoryRangeDate(
      this.state.selectedStartDate,
      this.state.selectedEndDate
    );
  };

  render() {
    return (
      <div style={styles.container}>
        <DatePicker
          style={styles.space}
          hintText="Start Date"
          container="inline"
          minDate={this.state.rangeStartDate}
          maxDate={this.state.selectedEndDate || this.state.rangeEndDate}
          value={this.state.selectedStartDate}
          onChange={this.changeStart}
        />
        <DatePicker
          hintText="End Date"
          container="inline"
          minDate={this.state.selectedStartDate || this.state.rangeStartDate}
          maxDate={this.state.rangeEndDate}
          value={this.state.selectedEndDate}
          onChange={this.changeEnd}
        />
      </div>
    );
  }
}
