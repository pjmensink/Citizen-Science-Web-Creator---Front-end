import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import { GoogleMap } from '../GoogleMap';
import { DynamicForm } from '../DynamicForm';
import { Modal } from '../Modal';

import formData from './data.json';
import styleData from './styles.json';

import { text } from './about.json'
import { text1 } from './about1.json'
import { text2 } from './about2.json'
import { text4 } from './about4.json'
import { url } from './background.json'
import { image } from './image.json'
import { titlename } from './title.json'

import './inputForm.css'; //Stylesheet for the data input form
import './modal.css'; //Stylesheet for the modal window

class HomePage extends React.Component {
  
	constructor(props) {
		super(props);
		// State contains data to be submitted
		this.state = {
						loc: '',
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
		this.closeModal = this.closeModal.bind(this);
	}
	
	// Handle user input into all form inputs
	handleChange(event) {
		const target =  event.target;
		const value = target.value;
		const name = target.name
		// Update state to new value
		this.setState({
			[name]: value
		});
	}
	
	//Handle submission of form data
	handleSubmit(event) {
		event.preventDefault();

		this.setState({ submitted: true });
		
		// Get data to be submitted from state
		const loc = this.state.loc;
		const lat = this.state.lat;
		const lng = this.state.lng;
		const species = this.state.species;
		const common = this.state.common;
		const size = this.state.size + "\"";
		const conditions = this.state.conditions;
		const date = this.state.date;
		const imageURL = this.state.photo.split("\\").pop(); // Retrive just file name
		const { dispatch } = this.props;
		dispatch(userActions.submit(loc, size, conditions, date, imageURL, lat, lng, species, common));	// Dispatch a submit data request
		dispatch(userActions.submitImage(this.uploadInput.files[0], this.state.photo.split("\\").pop().split(".")[0])); // Dispate a submit image request
	}
	
	// Handle select location event
	chooseLoc(event) {
		event.preventDefault();
		this.setState( {showMap: true} ); // Display the google map component to select a location
	} 
	
	// Handler for map click
	handleClick(latitude, longitude) {
		this.setState( {showMap: false} ); //Hide map after location chosen
		//Update location data
		this.setState( {lat: latitude} );
		this.setState( {lng: longitude} );
	}
	
	closeModal() {
		this.setState( {showMap: false} ); // Close modal
	}
	
	onSubmit(model){
		console.log(model);
		const { dispatch } = this.props;
		dispatch(userActions.submit(model));	// Dispatch a submit data request
		//const imageURL = this.state.photo.split("\\").pop(); // Retrive just file name
		//dispatch(userActions.submitImage(this.uploadInput.files[0], this.state.photo.split("\\").pop().split(".")[0])); // Dispatch a submit image request
	}
	
	render() {
		const { user, users, hist } = this.props;
		console.log(formData);
		return (
			<div>
			<div style={{"backgroundImage": "url("+url+")", "height": "700px"}}>
				{/*}<Modal show={this.state.showMap} handleClose={this.closeModal.bind(this)}>
					<GoogleMap size={{ height: '80%', width: '100%' }} handleClick={this.handleClick.bind(this)} center={{lat: 42, lng: -81}} zoom={3}/> 
				</Modal>
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
				</div>{*/}
				{/*}<div style={{"position": "relative", "top": "100px", "margin": "10px auto"}}><h1 style={{"fontFamily": "arial", "color": "yellow"}}><b>OCEAN EYES</b></h1></div>{*/}
				<DynamicForm className="form"
				  title={ titlename }
				  model={
					formData
				  }
				  className={styleData["style"]}
				  onSubmit = {(model) => {this.onSubmit(model)}} 
				/>
			</div>
			
			<div style={{"float": "left", "margin": "5px", "width": "40%"}}>
					<div style={{"position": "relative", "bottom": "5px"}}><h2><b></b></h2><p style={{"fontSize": "25px", "word-wrap": "break-word", "white-space": "nowrap", "overflow": "hidden"}}>{text}</p></div>
			</div>
			<div style={{"float": "right", "margin": "5px", "width": "40%"}}>
					<div style={{"position": "relative", "bottom": "5px"}}><h2><b></b></h2><p style={{"fontSize": "25px", "word-wrap": "break-word", "white-space": "nowrap", "overflow": "hidden"}}>{text1}</p></div>
			</div>
			<div style={{"float": "left", "margin": "5px", "width": "40%"}}>
					<div style={{"position": "relative", "bottom": "5px"}}><h2><b></b></h2><p style={{"fontSize": "18px", "word-wrap": "break-word"}}>{text2}</p></div>
			</div>
			<div style={{"float": "right", "margin": "5px", "width": "40%"}}>
				<div style={{"position": "relative", "bottom": "5px"}}><h2><b></b></h2><p style={{"fontSize": "18px", "display": "inline", "white-space": "nowrap", "word-wrap": "break-word"}}>{text4}</p></div>
				<div style={{"backgroundImage": "url("+image+")", "height": "200px", "width": "200px", "background-size": "cover", "display": "inline-block", "white-space": "nowrap"}}></div>
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
