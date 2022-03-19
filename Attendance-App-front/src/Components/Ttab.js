import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import SwipeableViews from 'react-swipeable-views';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Myclasscard from './Myclasscard';
import Mysubjectcard from './Mysubjectcard';

function TabContainer({ children, dir }) {
  return (
    <Typography component="div" dir={dir} style={{ padding: 8 * 3 }}>
      {children}
    </Typography>
  );
}

TabContainer.propTypes = {
  children: PropTypes.node.isRequired,
  dir: PropTypes.string.isRequired,
};

const styles = theme => ({
  root: {
    backgroundColor: theme.palette.background.paper,
    minWidth: 400,
    maxWidth:1100,
    margin:'auto'
  },
});

class Ttab extends React.Component {
  state = {
    value: 0,
    steacher:true,
    cteacher:true,
  };

  handleChange = (event, value) => {
    this.setState({ value });
  };

  handleChangeIndex = index => {
    this.setState({ value: index });
  };

  render() {
    const { classes, theme } = this.props;

    return (
      <div className={classes.root}>
      
        <AppBar position="static" color="default">
          <Tabs
            value={this.state.value}
            onChange={this.handleChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
          >
            <Tab label="MY SUBJECT" style={{fontFamily:'Arial',fontSize:18,color:'black'}} />
            <Tab label="MY CLASS" style={{fontFamily:'Arial', fontSize:18,color:'black'}} />
          </Tabs>
        </AppBar>
        <SwipeableViews
          axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
          index={this.state.value}
          onChangeIndex={this.handleChangeIndex}
          
        >
          <TabContainer dir={theme.direction}>
            <Mysubjectcard />
          </TabContainer>
          <TabContainer  dir={theme.direction}><Myclasscard /></TabContainer>
        </SwipeableViews>
      </div>
    );
  }
}

Ttab.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(Ttab);
