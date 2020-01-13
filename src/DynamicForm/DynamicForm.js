import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';
import { GoogleMap } from '../GoogleMap';
import { Modal } from '../Modal';
import './modal.css'; //Stylesheet for the modal window
import './Dynamic.css';

import { color } from '../HomePage/color.json'
import { font } from '../HomePage/font.json'
import { fontcolor } from '../HomePage/fontcolor.json'

class DynamicForm extends React.Component {
	
    constructor(props) {
        super(props);
        this.state ={};
        console.log(this.state);
        this.showMap = false;
        this.onChange = this.onChange.bind(this);
		this.onSubmit = this.onSubmit.bind(this);
    }
	
	closeModal() {
		this.showMap = false;
	}
	
	// Handler for map click
	handleClick(latitude, longitude) {
		closeModal();
		//Update location data
		this.setState( {lat: latitude} );
		this.setState( {lng: longitude} );
	}
	
	// Handle select location event
	chooseLoc(event) {
		event.preventDefault();
		this.showMap = true; // Display the google map component to select a location
	} 
	
	
    onSubmit(e) {
        e.preventDefault();
	console.log("state" + this.state);
        if (this.props.onSubmit) this.props.onSubmit(this.state);
    }

    // Handle user input into all form inputs
	onChange(event) {
		const target =  event.target;
		const value = target.value;
        console.log(target);
        console.log("heree");
        console.log(value);
		const name = target.name
		// Update state to new value
		this.setState({
			[name]: value
		});
	}


    renderForm() {
        let model = this.props.model;
        let defaultValues = this.props.defaultValues;
        
        let formUI = model.map((m) => {
            let key = m.key;
            let type = m.type || "text";
            let props = m.props || {};
            let name= m.name;
            console.log(name);
            let value = "empty";
            console.log(value);
            let min = m.min;
            let max = m.max;
            let className = m.className || "form-input";
            let groupName = m.groupName || "form-group";

            let target = key;
            value = this.state[target];
            value = "empty";

            let input =  <input {...props}
                    className={className}
                    type={type}
                    key={key}
                    name={name}
                    defaultValue={value}
                    onChange={(e)=>{this.onChange(e)}}
                />;

            if (type == "radio") {
               input = m.options.map((o) => {
                   let checked = o.value == value;
                    return (
                        <React.Fragment key={'fr' + o.key}>
                            <input {...props}
                                    className="form-input"
                                    type={type}
                                    key={o.key}
                                    name={name}
                                    checked={this.props.checked}
                                    defaultValue={o.value}
                                    onChange={(e)=>{this.onChange(e, o.name)}}
                            />
                            <label key={"ll" +o.key }>{o.label}</label>
                        </React.Fragment>
                    );
               });
               input = <div className ="form-group-radio" type="radio">{input}</div>;
            }

            if (type == "select") {
		
                input = m.options.map((o) => {
                    let checked = o.value == value;
                    console.log("select: ", o.value, value);
                     return (
                            <option {...props}
                                className="form-input"
                                type={type}
                                key={key}
                                name={name}
                                checked={checked}
                                defaultValue={o.value}
                            >{o.value}</option>
                     );
                });

                input = <select value={value} onChange={(e)=>{this.onChange(e, m.key)}}>{input}</select>;
		
		
             }

             if (type == "checkbox") {
                input = m.options.map((o) => {
                    
                    //let checked = o.value == value;
                    let checked = false;
                    if (value && value.length > 0) {
                        checked = value.indexOf(o.value) > -1 ? true: false;
                    }
                    console.log("Checkbox: ",checked);
                     return (
                        <React.Fragment key={"cfr" + o.key}>
                            <input {...props}
                                className="form-input"
                                type="checkbox"
                                key={o.key}
                                name={name}
                                checked={checked}
                                defaultValue={o.value}
                                onChange={(e)=>{this.onChange(e, m.key,"multiple")}}
                            />
                            <label key={"ll" +o.key }>{o.label}</label>
                        </React.Fragment>
                     );
                });

                input = <div className ="form-group-checkbox"> {input}</div>;

             }
             
            if (type == "range") {
				input =<input {...props}
                    className={className}
                    type={type}
                    key={key}
                    name={name}
                    defaultValue={value}
                    min={min}
                    max={max}
                    onChange={(e)=>{this.onChange(e)}}
                />;
			}
			
			if (type == "map") {
				input =  <div><Modal show={this.state.showMap} handleClose={this.closeModal.bind(this)}>
							<GoogleMap size={{ height: '80%', width: '100%' }} handleClick={this.handleClick.bind(this)} center={{lat: 42, lng: -81}} zoom={3}/> 
						</Modal>
						<button style={{"height":"30px","fontWeight":"bold","color":"white","background":"rgb(26, 188, 156)"}}type="button" onClick={this.chooseLoc.bind(this)}>Select Location</button></div>;
			}
			
			if (type == "imageUpload") {
				
				input = <div><div>
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
							<hr /></div>;
			}
			
            return (
                <div key={'g' + key} className={groupName}>
                    <label className="form-label"
                        key={"l" + key}
                        htmlFor={key}>
                        {m.label}
                    </label>
                    {input}
                </div>
            );
        });
        return formUI;
    }

    render () {
        let title = this.props.title || "Dynamic Form";

        return (
            <div className={this.props.className} id="formTemplate" style={{"background": color, "font-family": font, "color": fontcolor}}>
                <h3 className="form-title">{title}</h3>
                <form className="dynamic-form" onSubmit={(e)=>{this.onSubmit(e)}}>
                    {this.renderForm()}
                    <div className="form-actions">
                        <button type="submit">submit</button>
                    </div>
                </form>
            </div>
        )
    }
 
}

function mapStateToProps(state) {
    const { authentication } = state;
    const { user } = authentication;
    return {
        user
    };
}

const connectedDynamicForm = connect(mapStateToProps)(DynamicForm);
export { connectedDynamicForm as DynamicForm };
