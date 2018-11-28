import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import HomePage from './HomePage/HomePage'
import LoginPage from './Login/LoginPage'
import './App.css';
//import logo from './ocean-eyes-logo.png';

class App extends Component {

  render() {
    return (
      <div className="App">
        <header className="App-header">
        </header>
		  <div>
		    <BrowserRouter>
		      <Switch>
				<Route exact path="/home" component={HomePage}/>
				<Route path="/" component={LoginPage}/>
			  </Switch>
			</BrowserRouter>
		  </div>
      </div>
    );
  }
}

export default App;
