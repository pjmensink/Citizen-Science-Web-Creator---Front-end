import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import ReactTable from "react-table";

import 'react-table/react-table.css'

import { CSVLink, CSVDownload } from "react-csv";

class DataPage extends React.Component {
	
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

	const columns = [{
		Header: 'Location',
		accessor: 'location' 
	}, {
		Header: 'Latitude',
		accessor: 'latitude'
	}, {
		Header: 'Longitude',
		accessor: 'longitude'
	}, {
		Header: 'Date',
		accessor: 'date'
	}, {
		Header: 'Species',
		accessor: 'species'
	}, {
		Header: 'Common Name',
		accessor: 'common'
	}, {
		Header: 'Catch Size',
		accessor: 'catch_size'
	}, {
		Header: 'Conditions', 
		accessor: 'conditions'
	}, {
		Header: 'Image', 
		accessor: 'img'
	}]
	
    return (

			<div>
				{hist.items &&
					<ReactTable className="-striped -highlight"
						data={hist.items}
						columns={columns}
						filterable={true}
					/>	
				}
				{hist.items &&<CSVLink data={hist.items}>Download me</CSVLink>}
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

const connectedDataPage = connect(mapStateToProps)(DataPage);
export { connectedDataPage as DataPage };
