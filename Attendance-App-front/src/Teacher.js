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
              <form >
              </form>
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
