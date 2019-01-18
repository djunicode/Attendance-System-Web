import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Link
} from 'react-router-dom';
import PersistentDrawerLeft from './Components/PersistentDrawerLeft';
import Subject from './Subject';
import Student from './Student';
import Teacher from './Teacher';

class App extends Component {
  render() {
    return (
      <Router>
         <div>
           <PersistentDrawerLeft />
     
      <Switch>
        <Route exact path="/Student" component={Student} />
        <Route exact path="/Teacher" component={Teacher} />
        <Route exact path="/Subject" component={Subject} />



      </Switch>
      </div>
      </Router>
     
    );
  }
}

export default App;
