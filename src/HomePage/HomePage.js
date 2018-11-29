import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';


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
                  imageURL: ''
                  };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleUploadImage = this.handleUploadImage.bind(this);
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
    const imageURL = this.state.imageURL;
    const { dispatch } = this.props;
    dispatch(userActions.submit(loc, size, conditions, date, imageURL));
  }
  
  handleUploadImage(event) {
    event.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    fetch('http://localhost:4000/upload', {
      method: 'POST',
      body: data
    }).then(response => {
      response.json().then(body => {
        this.setState({ imageURL: `http://localhost:8000/${body.file}` });
      });
    });
  }
  
  render() {
	const { user, users } = this.props;
    return (
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
				<input type="submit" value="Submit" />
          </form>
          
          <h1>FileUpload</h1>
		<form onSubmit={this.handleUploadImage}>
			<div>
				<input
					ref={ref => {
						this.uploadInput = ref;
					}}
					type="file"
				/>
			</div>
			<br />
			<div>
			<input
				ref={ref => {
					this.fileName = ref;
				}}
				type="text"
				placeholder="Enter the desired name of file"
			/>
			</div>
			<br />
			<div>
				<button>Upload</button>
			</div>
			<hr />
			<p>Uploaded Image:</p>
			<img style={{"height" : "50px", "width" : "100px"}} src={this.state.imageURL} alt="img" />
		</form>
        </div>
      
    );
  }
}

function mapStateToProps(state) {
    const { users, authentication } = state;
    const { user } = authentication;
    return {
        user,
        users
    };
}

const connectedHomePage = connect(mapStateToProps)(HomePage);
export { connectedHomePage as HomePage };
