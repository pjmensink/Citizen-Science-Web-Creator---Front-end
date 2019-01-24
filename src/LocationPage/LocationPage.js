import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import { GoogleMap } from '../GoogleMap';

class LocationPage extends React.Component {
	
  componentDidMount() {
        this.props.dispatch(userActions.getHistory());
  }
  
  handleDeleteUser(id) {
        return (e) => this.props.dispatch(userActions.delete(id));
  }
  
  constructor(props) {
    super(props);
  }
  
  render() {
	const { user, users, hist } = this.props;
	
    return (

			<div>
				<GoogleMap size={{ height: '100vh', width: '100%' }} data={hist.items} center={{lat: 42, lng: -81}} zoom={5}/> 
			</div>	
    );
  }
}

function mapStateToProps(state) {
    const { hist, users, authentication } = state;
    const { user } = authentication;
    return {
        user,
        users,
        hist
    };
}

const connectedLocationPage = connect(mapStateToProps)(LocationPage);
export { connectedLocationPage as LocationPage };
