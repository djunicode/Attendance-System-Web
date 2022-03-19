import React from 'react';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';
import {Grid , Paper , Typography, TextField, Button, MenuItem, Select, InputLabel, FormControl} from '@material-ui/core';
import PropTypes, { nominalTypeHack } from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { createMuiTheme, MuiThemeProvider} from '@material-ui/core/styles';

const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  Grid: {
    padding: theme.spacing.unit * 2,
    textAlign: 'center',
  },
  text: {
    color: 'black',
  },
  button: {
    margin: 40,
    padding: 2,
    height: 50,
    width: 300,

  }
});

function typographyV1Theme(theme) {
  return createMuiTheme({
    ...theme,
    typography: {
      useNextVariants: false,
    },
  });
}


class Teacher extends React.Component{
  state={age: ''}

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };
  
  render(){
    const { classes } = this.props;

    return (
      <div className={classes.root}>
        <Grid container spacing={12} className={classes.Grid}>
          <Grid item xs> 
          </Grid>
          <Grid item xs>
            <div>
              <Typography component="h2" variant="display3" gutterBottom className={classes.text}>Teacher</Typography>
            </div>
            <div>
              <form autoComplete="off">
                <Grid container spacing={24}>
                  <Grid item xs={6}>
                    <TextField
                    id="outlined-name"
                    label="First Name"
                    value={this.state.name}
                    margin="normal"
                    variant="outlined"
                    fullWidth />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                    id="outlined-name"
                    label="Surname"
                    value={this.state.name}
                    margin="normal"
                    variant="outlined"
                    fullWidth />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      id="outlined-name"
                      label="User"
                      value={this.state.name}
                      margin="normal"
                      variant="outlined"
                      fullWidth />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      id="outlined-name"
                      label="Specialisation"
                      value={this.state.name}
                      margin="normal"
                      variant="outlined"
                      fullWidth />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      id="outlined-name"
                      label="Teacher-ID"
                      value={this.state.name}
                      margin="normal"
                      variant="outlined"
                      fullWidth />
                  </Grid>
                  <Grid item xs>
                    <FormControl>
                      <InputLabel htmlFor="age-simple">Subject</InputLabel>
                      <Select style={{width:150}}
                      value={this.state.age}
                      onChange={this.handleChange}
                      inputProps={{
                      name: 'age',
                      id: 'age-simple',
                      }}>
                        <MenuItem value=""><em>None</em></MenuItem>
                        <MenuItem value={10}>OS</MenuItem>
                        <MenuItem value={20}>AOA</MenuItem>
                        <MenuItem value={20}>COA</MenuItem>
                        <MenuItem value={20}>OSL</MenuItem>
                        <MenuItem value={20}>Maths</MenuItem>
                        <MenuItem value={20}>CG</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </Grid>
              </form>
              <div>
                <Button variant="contained" color="primary"  className={classes.button}>Submit</Button>
              </div>
            </div>
          </Grid>
          <Grid item xs>
          </Grid>
        </Grid>
      </div>
    );
  }
}

Teacher.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Teacher);
