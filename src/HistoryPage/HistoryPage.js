import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

class HistoryPage extends React.Component {
	
  componentDidMount() {
        this.props.dispatch(userActions.getAll());
        this.props.dispatch(userActions.getHistory());
  }
  
  handleDeleteUser(id) {
        return (e) => this.props.dispatch(userActions.delete(id));
  }
  
  constructor(props) {
    super(props);
  }
  
  render() {
	const { user, users, hist } = this.props;
    return (

			<div>
				
				{hist.items &&
					<table style={{"borderWidth":"1px", 'borderStyle':'solid'}}>
					<thead>
						<tr>
							<th style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>Location</th>
							<th style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>Date</th>
							<th style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>Size</th>
							<th style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>Conditions</th>
							<th style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>Image</th>
						</tr>
                        {hist.items.map((item, index) =>
                           <tr key={item._id}>
								<td style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>{item.location}</td>
								<td style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>{item.date}</td>
								<td style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>{item.catch_size}</td>
								<td style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>{item.conditions}</td>
								<td style={{"borderWidth":"1px", 'borderStyle':'solid', 'padding':'5px', 'textAlign':'center'}}>{item.imageURL}</td>
                            </tr>
                        )}
					</thead>
					</table>
				}
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

const connectedHistoryPage = connect(mapStateToProps)(HistoryPage);
export { connectedHistoryPage as HistoryPage };
