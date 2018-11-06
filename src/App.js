import React, { Component } from 'react';
import './App.css';
//import logo from './ocean-eyes-logo.png';

class App extends Component {
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

  handleSubmit(event) {
    event.preventDefault();
    
    const data = new FormData();
	data.append('location', this.state.loc);
	data.append('catch_size', this.state.size);
	data.append('conditions', this.state.conditions);
	data.append('date', this.state.date);

	fetch('http://localhost:8000/test', {
		method: 'POST',
		body: data
		}).then(response => {
			response.json().then(body => {
			this.setState();
		});
	});
  }
  
  handleUploadImage(event) {
    event.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: data
    }).then(response => {
      response.json().then(body => {
        this.setState({ imageURL: `http://localhost:8000/${body.file}` });
      });
    });
  }
  
  render() {
    return (
      <div className="App">
        <header className="App-header">
        </header>
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
			<img src={this.state.imageURL} alt="img" />
		</form>
        </div>
      
      </div>
    );
  }
}

export default App;
