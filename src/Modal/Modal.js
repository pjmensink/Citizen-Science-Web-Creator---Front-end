import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

class Modal extends React.Component {

  render() {
	const showHideClassName = this.props.show ? "modal display-block" : "modal display-none";
	
    return (
		<div className={showHideClassName}>
		  <section className="modal-main">
			{this.props.children}
			<button onClick={this.props.handleClose}>close</button>
		  </section>
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

const connectedModal = connect(mapStateToProps)(Modal);
export { connectedModal as Modal };
