import React from 'react';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Select from '@material-ui/core/Select';
import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import PropTypes  from 'prop-types';
import { withStyles, withTheme } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

const styles = theme => ({
  root: {
    margin:'auto',
    maxWidth:550,
    flexWrap: 'wrap',
    textAlign:'center',
    // [theme.breakpoints.down('md')]:{
    //   width:'100%'
    // }
  },
  formControl: {
    width:200,
    fontSize:16 
  },
  
  button: {
    color:'white',
    padding: 15,
    margin: 20,
    width: 300,
    fontSize:18,
    '&:hover': {
      backgroundColor: '#0288d1',
      color:'white'
    }
  },
  paper: {
   padding:25, 
  },
  intro: {
    display: 'flex'
  },
  
});

class Subject extends React.Component {

  state = {
    age: '',

  };

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root} >
        <PersistentDrawerLeft />
        <Paper className={classes.paper}>
       
        <form  autoComplete="off">
        <div>
              <Typography component="h2" variant="h3" align="center"  gutterBottom className={classes.text}>SUBJECT </Typography>
            </div>
        

        <FormControl className={classes.formControl}>
          <Select
            value={this.state.age}
            onChange={this.handleChange}
            name="age"
            displayEmpty
            className={classes.selectEmpty}
          >
            <MenuItem value="" disabled>
              Semester
            </MenuItem>
            <MenuItem value={1}>  Semester 1</MenuItem>
            <MenuItem value={2}>  Semester 2</MenuItem>
            <MenuItem value={3}>  Semester 3</MenuItem>
            <MenuItem value={4}>  Semester 4</MenuItem>
            <MenuItem value={5}>  Semester 5</MenuItem>
            <MenuItem value={6}>  Semester 6</MenuItem>
            <MenuItem value={7}>  Semester 7</MenuItem>
            <MenuItem value={8}>  Semester 8</MenuItem>
          </Select>
          
        </FormControl>
       
        <TextField style={{ width: 500 }}
          
          id="subject"
          label="Subject"
          type="text"
          name="subject"
          margin="normal"
          variant="outlined"
        />


        
        <TextField style={{ width: 500 }}
          id="subject-code"
          label="Subject-code"
          type="text"
          name="subject-code"
          margin="normal"
          variant="outlined"
        />
           
        <div className={classes.intro}>
          <Button variant="contained" color="secondary" className={classes.button}>Submit</Button>
          <Button variant="contained" color="secondary" className={classes.button}>Proceed</Button>
        </div>
        </form>
        </Paper>

        
       
        
          
      </div>
    );
  }
}

Subject.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Subject);

