
import React from 'react';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';
import OutlinedTextFields from './Components/OutlinedTextFields';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Select from '@material-ui/core/Select';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import PropTypes, { nominalTypeHack } from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';

const styles = theme => ({
    root: {
      
      display: 'flex',
      flexWrap: 'wrap',
    },
   
    formControl: {
      margin: theme.spacing.unit,
      minWidth: 200,
    },
    selectEmpty: {
      marginTop: theme.spacing.unit * 2,
    },
    button:{
      
        padding:20,
        margin:20,
        width:300,
        '&:hover': {
            backgroundColor:'black',
        }
    },
    paper: {
      display:'flex',
      width:10,
      padding: theme.spacing.unit * 2,
      textAlign: 'center',
      color: theme.palette.text.secondary,
      
      
      
    },
    intro:{
      display:'flex'
    }
  });

class Subject extends React.Component{

    state = {
        age: '',
       
      };
    
    
    
      handleChange = event => {
        this.setState({ [event.target.name]: event.target.value });
      };
    render(){
        const { classes } = this.props;
        return(
            <div className="App-header">
       <PersistentDrawerLeft />

          
             <h1 className="title">Subject</h1>
       
           

            
         <TextField style={{width:500}}
          id="subject"
          label="Subject"
          type="text"
          name="subject"
          margin="normal"
          variant="outlined"
        />
         <TextField style={{width:500}}
          id="subject-code"
          label="Subject-code"
          type="text"
          name="subject-code"
          margin="normal"
          variant="outlined"
        />
        <form className={classes.root} autoComplete="off">
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="age-simple">Semester</InputLabel>
          <Select
            value={this.state.age}
            onChange={this.handleChange}
            inputProps={{
              name: 'age',
              id: 'age-simple',
            }}
          >
            
            <MenuItem value={1}>Semester 1</MenuItem>
            <MenuItem value={2}>Semester 2</MenuItem>
            <MenuItem value={3}>Semester 3</MenuItem>
            <MenuItem value={3}>Semester 4</MenuItem>
            <MenuItem value={3}>Semester 5</MenuItem>
            <MenuItem value={3}>Semester 6</MenuItem>
            <MenuItem value={3}>Semester 7</MenuItem>
            <MenuItem value={3}>Semester 8</MenuItem>

          </Select>
        </FormControl>
        </form>
        <div className={classes.intro}>
        <Button variant="contained" color="primary" className={classes.button}>Submit</Button>
        <Button variant="contained" color="primary" className={classes.button}>Proceed</Button>
        </div>
      
       


            </div>
        );
    }
}

Subject.propTypes = {
    classes: PropTypes.object.isRequired,
  };
  
  export default withStyles(styles)(Subject);
