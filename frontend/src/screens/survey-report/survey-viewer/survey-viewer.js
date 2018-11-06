import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
// import Resizable from 're-resizable';
import QlfApi from '../../../containers/offline/connection/qlf-api';

const apiUrl = process.env.REACT_APP_API;

const styles = {
  iframe: {
    height: 'calc(100vh - 135px)',
    width: 'calc(100vw - 64px - 12vw)',
  },
  preview: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  previewContent: {
    width: '100%',
    display: 'grid',
    gridTemplateColumns: 'auto',
    height: 'calc(100vh - 135px)',
    overflowY: 'auto',
  },
  previewResize: {
    borderRight: '1px solid darkgrey',
    paddingRight: '10px',
    marginRight: '10px',
    overflow: 'hidden',
  },
  tableViewer: {
    overflowY: 'auto',
  },
  legend: {
    marginBottom: '10px',
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

class SurveyViewer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      objects: [],
      total: [],
      good: [],
      bad: [],
      startDate: '',
      endDate: '',
      program: '',
    };
  }
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

  // componentWillReceiveProps(nextProps) {
  //   if (
  //     nextProps.startDate !== this.state.startDate &&
  //     nextProps.endDate !== this.state.endDate &&
  //     nextProps.program !== this.state.program
  //   ) {
  //     this.fetchObjects(
  //       this.formatDate(nextProps.startDate),
  //       this.formatDate(nextProps.endDate),
  //       nextProps.program
  //     );
  //   }
  // }

  fetchObjects = async (startDate, endDate, program) => {
    this.setState({
      objects: [],
      total: [],
      good: [],
      bad: [],
      startDate: '',
      endDate: '',
      program: '',
    });
    const rows = await QlfApi.getObjectData(startDate, endDate, program);
    this.setState({
      objects: rows.objects,
      total: rows.total,
      good: rows.good,
      bad: rows.bad,
      startDate,
      endDate,
      program,
    });
  };

  formatDate = date => {
    if (date.includes('T') && date.includes('-')) {
      return date.split('T')[0].replace(/-/g, '');
    }
    return '';
  };

  renderImage = () => {
    const { classes } = this.props;
    let url = `${apiUrl}dashboard/get_footprint`;

    if (
      this.formatDate(this.props.startDate) !== '' &&
      this.formatDate(this.props.endDate) !== '' &&
      this.props.program !== ''
    )
      url = `${apiUrl}dashboard/get_footprint?start=${this.formatDate(
        this.props.startDate
      )}&end=${this.formatDate(this.props.endDate)}&program=${
        this.props.program
      }`;

    return (
      <div className={classes.previewContent}>
        {/* <Resizable
          className={classes.previewResize}
          defaultSize={{
            width: 'auto',
            height: 'auto',
          }}
        > */}
        <iframe
          title="image-modal"
          className={classes.iframe}
          frameBorder="0"
          src={url}
          onLoad={this.props.loadEnd}
        />
        {/* </Resizable> */}
        {/* {this.renderTable()} */}
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
            {this.state.objects.map((object, index) => {
              return (
                <TableRow className={classes.row} key={index}>
                  <CustomTableCell component="th" scope="row">
                    {object}
                  </CustomTableCell>
                  <CustomTableCell numeric>
                    {this.state.total[index]}
                  </CustomTableCell>
                  <CustomTableCell numeric>
                    {this.state.good[index]}
                  </CustomTableCell>
                  <CustomTableCell numeric>
                    {this.state.bad[index]}
                  </CustomTableCell>
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
    return <div className={classes.preview}>{this.renderImage()}</div>;
  }
}

export default withStyles(styles)(SurveyViewer);
