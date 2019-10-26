import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import GoogleMapReact from 'google-map-react';

const Marker = ({ text }) => (
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
    this.childClick = this.childClick.bind(this);
  }

  _onClick({x, y, lat, lng, event}) {
	  console.log(x, y, lat, lng, event);
	  if (this.props.handleClick)
		this.props.handleClick(lat, lng);
  }
  
  childClick(event, data) {
	console.log(data);
  }
  
  createMarkers(data) {
	let markers = [];
	var arrLen = data.length;
	for(var i = 0 ; i < arrLen ; i ++) {
		if(data[i]['latitude']){
			markers.push(<Marker 
			  lat={data[i]['latitude']} 
			  lng={data[i]['longitude']} 
			  text={'!'} 
			  key={i}
			  data={data[i]}
			/>
			);
		}
	}
	return markers;
  }
  render() {

    return (
      <div style={this.props.size}>
        <GoogleMapReact
          defaultCenter={this.props.center}
          defaultZoom={this.props.zoom}
          onClick={this._onClick}
          onChildClick={this.childClick}
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
