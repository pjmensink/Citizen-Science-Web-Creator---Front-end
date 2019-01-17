import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import GoogleMapReact from 'google-map-react';


const AnyReactComponent = ({ text }) => <div>{text}</div>;
 
class GoogleMap extends React.Component {
	
  
  constructor(props) {
    super(props);

    this._onClick = this._onClick.bind(this);
  }
  componentDidMount() {
        this.props.dispatch(userActions.getAll());
        this.props.dispatch(userActions.getHistory());
  }
  
  handleDeleteUser(id) {
        return (e) => this.props.dispatch(userActions.delete(id));
  }

  _onClick({x, y, lat, lng, event}) {
	  console.log(x, y, lat, lng, event);
	  this.props.handleClick(lat, lng);
  }
  
  render() {
    return (
      <div style={{ height: '100vh', width: '100%' }}>
        <GoogleMapReact
          defaultCenter={this.props.center}
          defaultZoom={this.props.zoom}
          onClick={this._onClick}
        >
          <AnyReactComponent 
            lat={42.238723}
            lng={-81.242077}
            text={'This is Lake Erie'}
          />
        </GoogleMapReact>
      </div>
    );
  }
}

function mapStateToProps(state) {
    const { users, authentication } = state;
    const { user } = authentication;
    return {
        user,
        users,
    };
}

const connectedGoogleMap = connect(mapStateToProps)(GoogleMap);
export { connectedGoogleMap as GoogleMap };
