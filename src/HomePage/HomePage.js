import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import { GoogleMap } from '../GoogleMap';

import './inputForm.css';

class HomePage extends React.Component {
	
  componentDidMount() {
        this.props.dispatch(userActions.getAll());
  }
  
  handleDeleteUser(id) {
        return (e) => this.props.dispatch(userActions.delete(id));
  }
  
  constructor(props) {
    super(props);
    this.state = {loc: '',
                  size: '1',
                  conditions: '',
                  date: '',
                  photo: '',
                  lat: '',
                  lng: '',
                  species: '',
                  common: '',
                  showMap: false
                  };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.chooseLoc = this.chooseLoc.bind(this);
  }

  handleChange(event) {
    const target =  event.target;
    const value = target.value;
    const name = target.name
    this.setState({
      [name]: value
    });
  }

  handleSubmit(e) {
    e.preventDefault();

    this.setState({ submitted: true });
    const loc = this.state.loc;
    const lat = this.state.lat;
    const lng = this.state.lng;
    const species = this.state.species;
    const common = this.state.common;
    const size = this.state.size;
    const conditions = this.state.conditions;
    const date = this.state.date;
    const imageURL = this.state.photo.split("\\").pop();
    const { dispatch } = this.props;
    dispatch(userActions.submit(loc, size, conditions, date, imageURL, lat, lng, species, common));
    dispatch(userActions.submitImage(this.uploadInput.files[0], this.state.photo.split("\\").pop().split(".")[0]));
  }
  
  chooseLoc(e) {
	e.preventDefault();
	this.setState( {showMap: true} );
  } 
  
  handleClick(latitude, longitude) {
	this.setState( {showMap: false} );
	this.setState( {lat: latitude} );
	this.setState( {lng: longitude} );
  }
  
  render() {
	const { user, users, hist } = this.props;
    return (
		<div>
		<div>
			 { this.state.showMap ? <GoogleMap handleClick={this.handleClick.bind(this)} center={{lat: 42, lng: -81}} zoom={11}/> : null }
		</div>
		<div className="form-style-5">
		
		<form onSubmit={this.handleSubmit}>
		<fieldset>
		<legend><span className="number">1</span> Catch Information</legend>
		<input style={{"width":"70%","marginRight":"5px" }}name="loc" type="text" placeholder="Catch Location" value={this.state.loc} onChange={this.handleChange} />
		<button style={{"height":"30px","fontWeight":"bold","color":"white","background":"rgb(26, 188, 156)"}}type="button" onClick={this.chooseLoc}>Select Location</button>
		<div>
		<input style={{"width":"49%","marginRight":"5px" }}name="species" type="text" placeholder="Species Name" value={this.state.species} onChange={this.handleChange} />
		<input style={{"width":"49%" }}name="common" type="text" placeholder="Common Name" value={this.state.common} onChange={this.handleChange} />
		</div>
		<div className="slidecontainer">
			<p>Catch Size: {this.state.size}"</p>
			<input name="size" type="range" min="1" max="60" className="slider" defaultValue="1" id="myRange" onChange={this.handleChange}/>
		</div>
		<textarea name="conditions" type="text" placeholder="Weather Conditions" value={this.state.conditions} onChange={this.handleChange}></textarea>
		<input name="date" type="date" placeholder="Date" value={this.state.date} onChange={this.handleChange} /> 
		</fieldset>
		<fieldset>
		<legend><span className="number">2</span> Image Upload</legend>
		<div>
				<input
					ref={ref => {
						this.uploadInput = ref;
					}}
					type="file"
					name='photo'
					onChange={this.handleChange}
				/>
			</div>
			<img style={{"height" : "50px", "width" : "100px"}} src={this.state.imageURL} />
			<hr />

		</fieldset>
		<input type="submit" value="Submit" style={{"fontWeight":"bold", "color":"white"}}/>
		</form>
		</div>
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

const connectedHomePage = connect(mapStateToProps)(HomePage);
export { connectedHomePage as HomePage };
