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
  label: {
    color: 'black',
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

  formatDate = date => {
    const month = (date.getMonth() + 1 < 10 ? '0' : '') + (date.getMonth() + 1);
    const day = (date.getDate() + 1 < 10 ? '0' : '') + date.getDate();
    return month + '/' + day + '/' + date.getFullYear();
  };

  render() {
    return (
      <div style={styles.container}>
        <DatePicker
          autoOk={true}
          style={styles.space}
          floatingLabelText="Start Date"
          floatingLabelStyle={styles.label}
          hintText="Start Date"
          container="inline"
          minDate={this.state.rangeStartDate}
          maxDate={this.state.selectedEndDate || this.state.rangeEndDate}
          value={this.state.selectedStartDate}
          onChange={this.changeStart}
          formatDate={this.formatDate}
        />
        <DatePicker
          autoOk={true}
          floatingLabelText="End Date"
          floatingLabelStyle={styles.label}
          hintText="End Date"
          container="inline"
          minDate={this.state.selectedStartDate || this.state.rangeStartDate}
          maxDate={this.state.rangeEndDate}
          value={this.state.selectedEndDate}
          onChange={this.changeEnd}
          formatDate={this.formatDate}
        />
      </div>
    );
  }
}
