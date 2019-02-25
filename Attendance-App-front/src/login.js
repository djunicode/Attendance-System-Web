import React from 'react';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

const styles = theme => ({
  root: {
    margin:'auto',
    maxWidth:550,
    flexWrap: 'wrap',
    textAlign:'center'
  },
  formControl: {
    width:300,
    fontSize:16
    
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2,
  },
  button: {
    padding: 20,
    margin: 20,
    width: 300,
    '&:hover': {
      backgroundColor: 'black',
    }
  },
  paper: {
   padding:25,

  },
  intro: {
    margin:'auto'
  },
  title:{
    maxWidth:500,
    margin:'auto', 
  }
});

class login extends React.Component {

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
        <h1>LOGIN</h1>      
        <TextField style={{ width: 500 }}
          id="name"
          label="Name"
          type="text"
          name="Name"
          margin="normal"
          variant="outlined"
        /> 
        <TextField style={{ width: 500 }}
          id="password"
          label="Password"
          type="password"
          name="password"
          margin="normal"
          variant="outlined"
        />    
        <div className={classes.intro}>
          <Button variant="contained" color="primary" className={classes.button}>Submit</Button>
        </div>
        </form>
        </Paper>         
      </div>
    );
  }
}
login.propTypes = {
  classes: PropTypes.object.isRequired,
};
export default withStyles(styles)(login);

