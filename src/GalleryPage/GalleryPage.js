import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

class GalleryPage extends React.Component {
	
  componentDidMount() {
        this.props.dispatch(userActions.getAll());
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

const connectedGalleryPage = connect(mapStateToProps)(GalleryPage);
export { connectedGalleryPage as GalleryPage };
