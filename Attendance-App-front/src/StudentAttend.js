import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { Paper, Grid } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';

const CustomTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
    fontSize: 20,
  },
  body: {
    fontSize: 16,
  },
}))(TableCell);

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
    ['@media (max-width:780px)']: { // eslint-disable-line no-useless-computed-key
      width: '100%!important'
    }
  },
  table: {
    minWidth: 400,
  },
  row: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.background.default,
    },
  },
  red: {
    color:  'red',
  },
  green: {
    color: 'green',
  },
});

let id = 0;
function createData(date,Name,p_a){
    id += 1;
  return { date, Name, p_a };
}

const rows = [
  createData('22/1/2019', 'Shail Shah', 'Present'),
  createData('21/1/2019', 'Shail Shah', 'Present'),
  createData('20/1/2019', 'Shail Shah', 'Present'),
  createData('19/1/2019', 'Shail Shah', 'Absent'),
  createData('18/1/2019', 'Shail Shah', 'Absent'),
];

class StudentAttend extends React.Component {
  render(){
    const { classes } = this.props;

    return (
      <div>
        <PersistentDrawerLeft />
        <Grid container>
          <Grid item xs={2}>
          </Grid>
          <Grid item xs={8}>
            <Grid container className={classes.table}>
              <Grid item xs={12}><Typography align='center' component="h2" variant="display3">Attendance for Shail Shah</Typography></Grid>
            </Grid>
              <Grid item xs={12} sm={12}>
                <Paper>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <CustomTableCell style={{fontSize:'1rem'}}>Date</CustomTableCell>
                        <CustomTableCell style={{fontSize:'1rem'}}>Present/Absent</CustomTableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {rows.map(row => (
                        <TableRow className={classes.row} key={row.id}>
                          <CustomTableCell component="th" scope="row">
                            {row.date}
                          </CustomTableCell>
                          {
                            row.p_a.toLowerCase() == "present" ? <CustomTableCell className={classes.green}>{row.p_a}</CustomTableCell> : <CustomTableCell className={classes.red}>{row.p_a}</CustomTableCell>
                          }
                          
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </Paper>
              </Grid>
            </Grid>
            <Grid item xs={2}>
            </Grid>
          </Grid>
      </div>
    );
  }
}

StudentAttend.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(StudentAttend);