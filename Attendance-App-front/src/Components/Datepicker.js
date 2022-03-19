import React from "react";
import DatePicker from "react-datepicker";
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import "react-datepicker/dist/react-datepicker.css";
import Button from '@material-ui/core/Button';
 
// CSS Modules, react-datepicker-cssmodules.css
// import 'react-datepicker/dist/react-datepicker-cssmodules.css';

const styles = theme => ({ 
    root:{
      margin:'auto',
      textAlign:'center',
      display:'flex'
    },

    date:{
      padding:'10px 5px',
      fontSize:20,
      textAlign:'center',
      width:175,
      borderRadius:5
    },
    button:{
      margin:'0px 10px',
      padding:6,
      '&:hover': {
        backgroundColor: 'black',
        color:'white'
      }
     
    }

})
 
class Datepicker extends React.Component {
  // constructor(props) {
  //   super(props);
  //   this.state = {
  //     startDate: new Date()
  //   };
  //   this.handleChange = this.handleChange.bind(this);
  // }

  state={
    startDate: new Date()
  }
 
  handleChange = (date) => {
    this.setState({
      startDate: date
    });

  }
  
  updateChange = () => {
    var completeDate=this.state.startDate;
    console.log(this.state.startDate);
    var date=completeDate.getDate();
    var month =completeDate.getMonth()+1;
    var year = completeDate.getFullYear();
    
        console.log(date +"/"+month+"/"+year);
    

  }
 
  render() {
    const{ classes }= this.props
    return (
      <div className={classes.root} >
        <DatePicker
        selected={this.state.startDate}
        onChange={this.handleChange}
        className={classes.date}
      />
     <br />
      <Button variant="outlined" color="primary" onClick={this.updateChange} className={classes.button}> Submit</Button>
      
      {/* {`${this.state.startDate}`} */}
      </div>
      
    );
  }
}

Datepicker.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Datepicker);