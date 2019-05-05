import React from 'react';
import { Router, Route, Link } from 'react-router-dom';
import { Redirect } from 'react-router';
import { connect } from 'react-redux';

import { history } from '../_helpers';
import { alertActions } from '../_actions';
import { HomePage } from '../HomePage';
import { LoginPage } from '../LoginPage';
import { RegisterPage } from '../RegisterPage';
import { HistoryPage } from '../HistoryPage';
import { LocationPage } from '../LocationPage';
import { GalleryPage } from '../GalleryPage';
import { DataPage } from '../DataPage';

class App extends React.Component {
    constructor(props) {
        super(props);

        const { dispatch } = this.props;
        history.listen((location, action) => {
            // clear alert on location change
            dispatch(alertActions.clear());
        });
    }

    render() {
        const { alert } = this.props;
        const loggedIn = localStorage.getItem('user');
        return (
            <div>
                <div>
                    <div>
                        
                        <Router history={history}>
							<div>

								<nav className="navbar navbar-default" style={{"marginBottom": "-10px"}}>
								  <ul className="nav navbar-nav" style={{"paddingTop": "5px"}}>
									{loggedIn&&<li><Link to={'/home'}> <p style={{"font-size": "20px"}}><b>Home</b></p> </Link></li>}
									{loggedIn&&<li><Link to={'/history'}><p style={{"font-size": "20px"}}><b>Upload History</b></p></Link></li>}
									{loggedIn&&<li><Link to={'/locations'}><p style={{"font-size": "20px"}}><b>Location History</b></p></Link></li>}
									{loggedIn&&<li><Link to={'/gallery'}><p style={{"font-size": "20px"}}><b>Gallery</b></p></Link></li>}				
								  </ul>
								  <ul className="nav navbar-nav navbar-right" style={{"paddingRight":"15px", "paddingTop": "5px"}}>
									<li><Link to={'/register'}><p style={{"font-size": "20px"}}>Signup</p></Link></li>
									{loggedIn&&<li><Link to={'/login'}><p style={{"font-size": "20px"}}>Logout</p></Link></li>}
									{!loggedIn&&<li><Link to={'/login'}><p style={{"font-size": "20px"}}>Login</p></Link></li>}
								  </ul>
								</nav>
								{alert.message &&
									<div className={`alert ${alert.type}`}>{alert.message}</div>
								}
								<Route exact path="/" render={() => (
								  loggedIn ? (
									<Redirect to="/home"/>
								  ) : (
									<Redirect to="/login"/>
								  )
								)}/>
                                <Route path="/home" component={HomePage} />
                                <Route path="/login" component={LoginPage} />
                                <Route path="/register" component={RegisterPage} />
                                <Route path="/history" component={HistoryPage} />
                                <Route path="/locations" component={LocationPage} />
                                <Route path="/gallery" component={GalleryPage} />
                                <Route path="/data" component={DataPage} />
                            </div>
                        </Router>
                    </div>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    const { alert } = state;
    return {
        alert
    };
}

const connectedApp = connect(mapStateToProps)(App);
export { connectedApp as App }; 
