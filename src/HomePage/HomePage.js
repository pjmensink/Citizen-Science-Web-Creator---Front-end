import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

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
                  size: '',
                  conditions: '',
                  date: '',
                  photo: ''
                  };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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
    const size = this.state.size;
    const conditions = this.state.conditions;
    const date = this.state.date;
    const imageURL = this.state.photo.split("\\").pop();
    const { dispatch } = this.props;
    dispatch(userActions.submit(loc, size, conditions, date, imageURL));
    dispatch(userActions.submitImage(this.uploadInput.files[0], this.state.photo.split("\\").pop().split(".")[0]));
  }
  
  render() {
	const { user, users, hist } = this.props;
    return (
		
		<div class="form-style-5">
		<form>
		<fieldset>
		<legend><span class="number">1</span> Catch Information</legend>
		<input name="loc" type="text" placeholder="Catch Location" value={this.state.loc} onChange={this.handleChange} />
		<input name="size" type="text" placeholder="Catch Size" value={this.state.size} onChange={this.handleChange} />
		<textarea name="conditions" type="text" placeholder="Weather Conditions" value={this.state.conditions} onChange={this.handleChange}></textarea>
		<input name="date" type="date" placeholder="Date" value={this.state.date} onChange={this.handleChange} /> 
		</fieldset>
		<fieldset>
		<legend><span class="number">2</span> Image Upload</legend>
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
			<hr />
			<p>Uploaded Image:</p>
			<img style={{"height" : "50px", "width" : "100px"}} src={this.state.imageURL} alt="img" />
		</fieldset>
		<input type="submit" value="Submit" style={{"font-weight":"bold", "color":"white"}}/>
		</form>
		</div>
		/*
        <div className="inputForm">
  
          <form onSubmit={this.handleSubmit}>
          
			<label>
				Location:<br/>
			<input name="loc" type="text" value={this.state.loc} onChange={this.handleChange} />
			</label>
	
			<br/>
			<label>
				Catch Size:<br/>
				<input name="size" type="text" value={this.state.size} onChange={this.handleChange} />
			</label><br/>
			<label>
				Conditions:<br/>
				<input name="conditions" type="text" value={this.state.conditions} onChange={this.handleChange} />
			</label><br/>
			<label>
				Date:<br/>
				<input name="date" type="date" value={this.state.date} onChange={this.handleChange} />
			</label><br/>
          
          <div>
			
		  </div>
          <h1>FileUpload</h1>
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
			<input type="submit" value="Submit" />
			<hr />
			<p>Uploaded Image:</p>
			<img style={{"height" : "50px", "width" : "100px"}} src={this.state.imageURL} alt="img" />
			
			</form>
        </div>
      */
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
