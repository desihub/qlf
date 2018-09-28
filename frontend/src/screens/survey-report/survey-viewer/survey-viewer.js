import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import FormLabel from '@material-ui/core/FormLabel';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const apiUrl = process.env.REACT_APP_API;

const styles = {
  iframe: {
    width: '45vw', //'calc(100vw - 710px)',
    height: 'calc(100vh - 151px)',
  },
  preview: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  previewcontent: {
    display: 'grid',
    gridTemplateColumns: 'auto auto',
    height: 'calc(100vh - 151px)',
  },
  tableViewer: {
    //width: '400px',
    display: 'grid',
    overflowY: 'auto',
    alignItems: 'start',
    //justifyContent: 'space-evenly',
    borderLeft: '1px solid darkgrey',
    paddingLeft: '10px',
    marginLeft: '10px',
  },
  button: {
    float: 'right',
  },
  spectrographLabel: {
    paddingBottom: 10,
  },
  main: {
    margin: '16px',
    padding: '16px',
  },
  row: {
    '&:nth-of-type(odd)': {
      backgroundColor: '#fafafa',
    },
  },
  green: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: '#008000',
    fontSize: 0,
    textIndent: '-9999em',
  },
  red: {
    display: 'inline-block',
    verticalAlign: 'top',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    border: 'solid 1px #333',
    background: '#ff0000',
    fontSize: 0,
    textIndent: '-9999em',
  },
};

const CustomTableCell = withStyles(() => ({
  head: {
    backgroundColor: '#cccccc',
    color: 'rgba(0, 0, 0, 0.87)',
    textTransform: 'uppercase',
    textAlign: 'left',
  },
  root: {
    paddingRight: '10px',
  },
  body: {
    textAlign: 'left',
  },
}))(TableCell);

let id = 0;

function createData(name, calories, fat, carbs, protein) {
  id += 1;
  return { id, name, calories, fat, carbs, protein };
}

const rows = [
  createData('Exposures', '40', '20 (50%)', '20 (50%)'),
  createData('LRG', '38', '20 (50%)', '20 (50%)'),
  createData('ELG', '41', '20 (50%)', '20 (50%)'),
  createData('STAR', '29', '20 (50%)', '20 (50%)'),
  createData('QSO', '20', '20 (50%)', '20 (50%)'),
  createData('SKY', '20', '20 (50%)', '20 (50%)'),
];

class SurveyViewer extends React.Component {
  static propTypes = {
    program: PropTypes.string,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    classes: PropTypes.object,
    loadEnd: PropTypes.func.isRequired,
  };

  componentDidMount() {
    document.title = 'Survey Report';
  }

  formatDate = date => {
    if (date.includes('T') && date.includes('-')) {
      return date.split('T')[0].replace(/-/g, '');
    }
    return '';
  };

  renderImage = () => {
    const { classes } = this.props;
    let url = '';

    if (
      this.formatDate(this.props.startDate) !== '' &&
      this.formatDate(this.props.endDate) !== '' &&
      this.props.program !== ''
    )
      url = `${apiUrl}dashboard/get_footprint/?start=${this.formatDate(
        this.props.startDate
      )}&end=${this.formatDate(this.props.endDate)}&program=${
        this.props.program
      }`;

    if (url !== '')
      return (
        <div className={classes.previewcontent}>
          <iframe
            title="image-modal"
            className={classes.iframe}
            frameBorder="0"
            src={url}
            onLoad={this.props.loadEnd}
          />
          {this.renderTable()}
        </div>
      );
  };

  renderTable = () => {
    const { classes } = this.props;

    return (
      <div className={classes.tableViewer}>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              <CustomTableCell />
              <CustomTableCell numeric>Total</CustomTableCell>
              <CustomTableCell numeric>
                Good <span className={classes.green}>Green</span>
              </CustomTableCell>
              <CustomTableCell numeric>
                Fail <span className={classes.red}>Red</span>
              </CustomTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map(row => {
              return (
                <TableRow className={classes.row} key={row.id}>
                  <CustomTableCell component="th" scope="row">
                    {row.name}
                  </CustomTableCell>
                  <CustomTableCell numeric>{row.calories}</CustomTableCell>
                  <CustomTableCell numeric>{row.fat}</CustomTableCell>
                  <CustomTableCell numeric>{row.carbs}</CustomTableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
    );
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.preview}>
        <FormLabel component="legend">Preview:</FormLabel>
        {this.renderImage()}
      </div>
    );
  }
}

export default withStyles(styles)(SurveyViewer);
