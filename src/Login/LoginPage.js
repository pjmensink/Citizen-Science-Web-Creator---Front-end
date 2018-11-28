import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import { Button } from 'react-bootstrap';
class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = {uname: '',
                  pass: '',
                  };
    this.routeChange = this.routeChange.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }
  
  routeChange(){
	if (this.state.uname === "admin" && this.state.pass === "admin") {
	  let path = `/home`;
      this.props.history.push(path);
	} else if(this.state.uname === "Nate" && this.state.pass === "admin"){
	  let path = `/home`;
      this.props.history.push(path);
	} else {
		alert("Invalid Login");
	}
  }
  
  handleChange(event) {
    const target =  event.target;
    const value = target.value;
    const name = target.name
    this.setState({
      [name]: value
    });
  }
  
  render() {
    return(
	    <div className="inputForm">
          <form onSubmit={this.handleSubmit}>
          
			<label>
				Username:<br/>
			<input name="uname" type="text" value={this.state.uname} onChange={this.handleChange}/>
			</label>
			<br/>
			<label>
				Password:<br/>
				<input name="pass" type="password" value={this.state.pass} onChange={this.handleChange}/>
			</label><br/>
          </form>
          <Button
            onClick={this.routeChange}
            block
            bsSize="large"
            type="submit"
          >
            Login
          </Button>
        </div>
    
    );
  }
}

export default withRouter(LoginPage)
