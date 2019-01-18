import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import GoogleMapReact from 'google-map-react';

const AnyReactComponent = ({ text }) => (
  <div style={{
    color: 'white', 
    background: 'red',
    padding: '15px 10px',
    display: 'inline-flex',
    textAlign: 'center',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '100%',
    transform: 'translate(-50%, -50%)'
  }}>
    {text}
  </div>
); 

class GoogleMap extends React.Component {
  
  constructor(props) {
    super(props);

    this._onClick = this._onClick.bind(this);
    this.createMarkers = this.createMarkers.bind(this);
  }
  componentDidMount() {
        this.props.dispatch(userActions.getAll());
  }

  _onClick({x, y, lat, lng, event}) {
	  console.log(x, y, lat, lng, event);
	  this.props.handleClick(lat, lng);
  }
  
  createMarkers(data) {
	let markers = [];
	var arrLen = data.length;
	for(var i = 0 ; i < arrLen ; i ++) {
		if(data[i]['latitude']){
			markers.push(<AnyReactComponent 
			  lat={data[i]['latitude']} 
			  lng={data[i]['longitude']} 
			  text={'!'} 
			  key={i}
			/>
			);
		}
	}
	return markers;
  }
  render() {

    return (
      <div style={{ height: '100vh', width: '100%' }}>
        <GoogleMapReact
          defaultCenter={this.props.center}
          defaultZoom={this.props.zoom}
          onClick={this._onClick}
        >
        { this.props.data ? this.createMarkers(this.props.data) : null }
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
