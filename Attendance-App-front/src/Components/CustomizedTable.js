import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { Link } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';

const CustomTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 16,
  },
}))(TableCell);

const styles = theme => ({
  root: {
   
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
    margin:'auto',
    ['@media (max-width:780px)']: { // eslint-disable-line no-useless-computed-key
        width: '100%!important'
      }
   
  },
  table: {
  minWidth:400,
  
   
  },
  row: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.background.default,
    },
  },
  red:{
    backgroundColor:'#d50000',
    color:'white',
    textAlign:'center!important'
  },
  green:{
    backgroundColor:'#00c853',
    color:'white',
    textAlign:'center!important'
  },
  tableCenter:{
    textAlign:'center!important',
    padding:'0px!important'
  }
  
  
});

let id = 0;
function createData(name, sap, percent) {
  id += 1;
  return { id, name, sap, percent };
}

const rows = [
  createData('Viram shah', 60004170122, 60),
  createData('vishal shah', 60004170123, 80),
  createData('Viraj shah', 60004170123, 74),
  createData('yash shah', 60004170124, 85),
  createData('vasu shah', 60004170125, 40)

];

class CustomizedTable extends React.Component {
    render(){
        const { classes } = this.props;
        return (
          // <Grid container>
          // <Grid item xs={12} sm={2}>
          // </Grid>
          // <Grid item xs={12} sm={8}>
          
          // </Grid>
          // <Grid item xs={12} sm={2}>
          // </Grid>
          // </Grid>

<Paper className={classes.root}>
            
<Table className={classes.table}>
  <TableHead>
    <TableRow >
      <CustomTableCell  className={classes.tableCenter} style={{fontSize:'1rem'}}>Name</CustomTableCell>
      <CustomTableCell    className={classes.tableCenter} style={{fontSize:'1rem'}}>Sap ID</CustomTableCell>
      <CustomTableCell  className={classes.tableCenter} style={{fontSize:'1rem'}}>Percentage</CustomTableCell>
    
    </TableRow>
  </TableHead>
  <TableBody >
    {rows.map(row => (

      <TableRow className={classes.row} key={row.id}>
        <CustomTableCell component="th" scope="row"  className={classes.tableCenter}>
      <Link to={`student/${row.sap}`} style={{textDecoration:'none',color:'black'}}>
          {row.name}
        </Link>
        </CustomTableCell>
        <CustomTableCell   className={classes.tableCenter} >{row.sap}</CustomTableCell>
        {
          row.percent > 75 ?  <CustomTableCell   className={classes.green} >{row.percent}</CustomTableCell> :  <CustomTableCell className={classes.red}   >{row.percent}</CustomTableCell>
        }
       
    
      </TableRow>
    ))}
  </TableBody>
</Table>
</Paper>
            
          );

    }


 
}

CustomizedTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CustomizedTable);
