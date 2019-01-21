import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

class GalleryPage extends React.Component {
	
  componentDidMount() {
        this.props.dispatch(userActions.getHistory());
        this.props.dispatch(userActions.getImages());
  }
  
  handleDeleteUser(id) {
        return (e) => this.props.dispatch(userActions.delete(id));
  }
  
  constructor(props) {
    super(props);
  }
  
  render() {
	const { user, users, hist, images } = this.props;

    return (

			<div>
				<img src={images.items} style={{"height" : "50px", "width" : "100px"}}/>
			</div>	
    );
  }
}

function mapStateToProps(state) {
    const { hist, images, users, authentication } = state;
    const { user } = authentication;
    return {
        user,
        users,
        hist,
        images
    };
}

const connectedGalleryPage = connect(mapStateToProps)(GalleryPage);
export { connectedGalleryPage as GalleryPage };
