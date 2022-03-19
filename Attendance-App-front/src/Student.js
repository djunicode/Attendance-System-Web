import React from 'react';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';
import {Grid, TextField, Paper, Button, Typography} from '@material-ui/core';
import PropTypes from 'prop-types';
import {createMuiTheme ,MuiThemeProvider} from '@material-ui/core';
import Input from '@material-ui/core/Input';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import FilledInput from '@material-ui/core/FilledInput';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const theme=createMuiTheme({
    typography: {
        useNextVariants: true,
      },
    palette:{
        primary:{
            main:"#445DFF"
        },
        secondary:{
            main:"#C1D37F"
        }
    }
}

);
const styles = theme => ({
    button: {
      margin: theme.spacing.unit,
    },
    input: {
      display: 'none',
    },
  });

class Student extends React.Component{
    state={ age:''}
    handleChange = event => {
        this.setState({ [event.target.name]: event.target.value });
      };
    render(){
        return(

            <Grid container justify="center" spacing={24}>
            <Grid item>
            <Paper style={{width:623}}>
            <h2 align="center">STUDENT</h2>

                <MuiThemeProvider theme={theme}>
            <form>
            <Grid container justify="center" spacing={24}>
            <Grid item xs={7}>
            <TextField
            id="outlined-name"
            label="First Name"
            value={this.state.name}
            margin="normal"
            variant="outlined"
            fullWidth />
            </Grid>
            {/* <Grid item xs={5}>
            </Grid>  */}
            <Grid item xs={7}>
            <TextField
            id="outlined-name"
            label="Last Name"
            value={this.state.name}
            margin="normal"
            variant="outlined"
            fullWidth />
            </Grid>
            <Grid item xs={7}>
            <TextField
            id="outlined-name"
            label="Sap Id"
            value={this.state.name}
            margin="normal"
            variant="outlined"
            fullWidth />
            </Grid>
            <Grid item xs={7}>
            <FormControl >
          <InputLabel htmlFor="age-simple" style={{width:850}}>Divison</InputLabel>
          <Select style={{width:150}}
            value={this.state.age}
            onChange={this.handleChange}
            inputProps={{
              name: 'age',
              id: 'age-simple',
            }}

          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            <MenuItem value={10}>A</MenuItem>
            <MenuItem value={20}>B</MenuItem>
          </Select>
        </FormControl>
        </Grid>
            <Grid item xs={7}></Grid>
            <Grid item xs={6}>
            <Button variant="contained" color="primary" style={{margin:'auto',display:'block'}}>
        SUBMIT
      </Button>
            </Grid>
    
            </Grid>
            </form>
            </MuiThemeProvider>
            </Paper>  
            </Grid>
            </Grid>
        );
    }
}

export default Student;