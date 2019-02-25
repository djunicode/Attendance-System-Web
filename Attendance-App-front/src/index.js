import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import purple from '@material-ui/core/colors/purple';
import green from '@material-ui/core/colors/green';
import cyan from '@material-ui/core/colors/cyan'; 
import yellow from '@material-ui/core/colors/yellow'

const theme = createMuiTheme({
    palette: {
      primary: {
          main:yellow[500]
      },
      secondary:{
          main:cyan[400]
      },
    },
    status: {
      danger: 'orange',
    },
  });


ReactDOM.render( <MuiThemeProvider theme={theme}><App /></MuiThemeProvider>, document.getElementById('root'));




// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
