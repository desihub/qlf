import React from 'react';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  card: {
    borderLeft: 'solid 4px #424242',
    flex: 1,
    margin: '1.5vh 1vw 1vh 1vw',
    minHeight: 30,
  },
  titleStyle: {
    fontSize: '1.2vw',
    color: 'rgba(0, 0, 0, 1)',
    padding: 4,
  },
  cardStyle: {
    padding: 0,
  },
};

class Cards extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    classes: PropTypes.object,
  };

  render() {
    const { classes } = this.props;
    return (
      <Card className={classes.card}>
        <CardHeader
          className={classes.cardStyle}
          classes={{ title: classes.titleStyle }}
          title={this.props.title}
        />
      </Card>
    );
  }
}

export default withStyles(styles)(Cards);
