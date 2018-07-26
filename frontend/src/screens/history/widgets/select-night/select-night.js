import React from 'react';
import Proptypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

const styles = {
  grid: {
    display: 'grid',
    gridTemplateAreas: "'title control control control'",
    alignItems: 'center',
  },
  select: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingBottom: '10px',
  },
  button: {
    minWidth: '10px',
  },
  value: {
    fontSize: '14px',
    textAlign: 'center',
    padding: '5px',
  },
  title: {
    paddingLeft: '10px',
    fontSize: '14px',
    color: 'rgba(0, 0, 0, 0.54)',
    gridArea: 'title',
  },
};

export default class SelectNight extends React.Component {
  static propTypes = {
    night: Proptypes.string,
    selectNight: Proptypes.func.isRequired,
  };

  render() {
    return (
      <div style={styles.grid}>
        <Typography variant="body2" style={styles.title}>
          Night:
        </Typography>
        <Button
          style={styles.button}
          onClick={() => this.props.selectNight('prev')}
        >
          {'<'}
        </Button>
        <Typography variant="body2" style={styles.value}>
          {this.props.night}
        </Typography>
        <Button
          style={styles.button}
          onClick={() => this.props.selectNight('next')}
        >
          {'>'}
        </Button>
      </div>
    );
  }
}
