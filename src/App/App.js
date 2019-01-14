import React from 'react';
import { Router, Route, Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { history } from '../_helpers';
import { alertActions } from '../_actions';
import { PrivateRoute } from '../_components';
import { HomePage } from '../HomePage';
import { LoginPage } from '../LoginPage';
import { RegisterPage } from '../RegisterPage';
import { HistoryPage } from '../HistoryPage';

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
        return (
            <div>
                <div>
                    <div>
                        
                        <Router history={history}>
							<div>
								<nav className="navbar navbar-default">
								  <ul className="nav navbar-nav">
									<li><Link to={'/'}> Home </Link></li>
									<li><Link to={'/history'}>Upload History</Link></li>
									<li><Link to={'/gallery'}>Gallery</Link></li>
									
								  </ul>
								  <ul className="nav navbar-nav navbar-right" style={{"paddingRight":"15px"}}>
									<li><Link to={'/register'}>Signup</Link></li>
									<li><Link to={'/login'}>Logout</Link></li>
								  </ul>
								</nav>
								{alert.message &&
									<div className={`alert ${alert.type}`}>{alert.message}</div>
								}
                                <PrivateRoute exact path="/" component={HomePage} />
                                <Route path="/login" component={LoginPage} />
                                <Route path="/register" component={RegisterPage} />
                                <Route path="/history" component={HistoryPage} />
                                <Route path="/gallery" component="" />
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
