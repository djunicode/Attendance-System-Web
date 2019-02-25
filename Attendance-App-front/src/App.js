import React, { Component } from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Switch,

} from 'react-router-dom';
import Subject from './Subject';
import Student from './Student';
import Teacher from './Teacher';
import AttendanceTable from './AttendanceTable';
import AttendanceStudent from './AttendaceStudent';
import Teachermain from './Teachermain';
import login from './login';
import AttendForDate from './AttendForDate';
import StudentAttend from './StudentAttend';
import { createMuiTheme } from '@material-ui/core/styles';
import purple from '@material-ui/core/colors/purple';
import green from '@material-ui/core/colors/green';
import EditPage from './EditPage';

const theme = createMuiTheme({
  palette: {
    primary: purple,
    secondary: green,
  },
  status: {
    danger: 'orange',
  },
});

class App extends Component {
  render() {
    return (
      <Router>
         <div>
       {/* <PersistentDrawerLeft /> */}
        
      <Switch>
        <Route exact path="/" component={login} />

        <Route exact path="/student" component={Student} />
        <Route exact path="/teacher" component={Teacher} />
        <Route exact path="/subject" component={Subject} />
        <Route exact path="/attendanceTable" component={AttendanceTable} />
        <Route exact path="/student/:id" component={AttendanceStudent} />
        <Route exact path="/teachermain" component={Teachermain} />
        <Route exact path="/attendfordate" component={AttendForDate} />
        <Route exact path="/StudentAttend" component={StudentAttend} />
        <Route exact path="/EditPage" component={EditPage} />
      </Switch>
      </div>
      </Router>     
    );
  }
}

export default App;
