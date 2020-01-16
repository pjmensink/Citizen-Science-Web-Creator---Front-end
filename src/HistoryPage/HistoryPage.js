import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { userActions } from '../_actions';

import ReactTable from "react-table";

import 'react-table/react-table.css'

class HistoryPage extends React.Component {
	
  componentDidMount() {
        this.props.dispatch(userActions.getAll());
        this.props.dispatch(userActions.getHistory());
        this.props.dispatch(userActions.getItems());
  }

  
  handleDeleteUser(id) {
        return (e) => this.props.dispatch(userActions.delete(id));
  }
  
  constructor(props) {
    super(props);
  }
  

  render() {
	const { user, users, hist, full } = this.props;


	
	var obj = hist.data;
	

	var x = -1;
	let output = [];
	let csvOutput = [];
	let finalList = [[]];
	let filteredName = [];
	let filteredData = [];
	const columns = [

	
	{
        Header: 'Data',
        id:'data',
        accessor: d => {
        	//let output = [
        	let outputWithin = []
        	//let i = 0;
			var arrayLength = this.props.hist.items.length;
        	for (var i = 0; i< arrayLength; i++) {
    			//if (this.props.hist.items[i].data !== 'undefined'){
    		
        	//for (let [key, value] of Object.entries(this.props.hist.items[i].data)) {
  			//outputWithin.push(`${key}:  ${value}` + " \ ");
			//		}
			for (const [key, value] of Object.entries(this.props.hist.items[i].data)) {
  			outputWithin.push('  ' + `${key} —   ${value}` );
			}
			output.push(outputWithin);
			//console.log(outputWithin);
  			outputWithin = [];
  			
			}
			x = x + 1;
			
			//if (x.indexOf(':') !== -1) {
  			//split and get
  			var y = toString(output[x]);
  			var spliter = toString(y.split(':')[1]);
  			console.log("yess");
  			var arrayOfStrings = output[x].toString().split('—');
  			//var arrayOfStringsAfter = arrayOfStrings.toString().split('||');

  			//console.log(arrayOfStringsAfter);
            //}
            
			csvOutput.push(arrayOfStrings.toString().split(','));
			var max = -Infinity;
			var index = -1;
			csvOutput.forEach(function(a, i){
			  if (a.length>max) {
			    max = a.length;
			    index = i;
			  }
			});
			//var myarray = ["nonsense", "goodpart", "nonsense2", "goodpar2t", "nonsense3", "goodpart3"],
			  filteredName = csvOutput[index].filter(function(el, index) {
			    // normally even numbers have the feature that number % 2 === 0;
			    // JavaScript is, however, zero-based, so want those elements with a modulo of 1:
			    return index % 2 === 0;
			  });

			for(var i = 0; i < csvOutput.length; i++){
			//var myarray = ["nonsense", "goodpart", "nonsense2", "goodpar2t", "nonsense3", "goodpart3"],
			  filteredData[i] = csvOutput[i].filter(function(el, index) {
			    // normally even numbers have the feature that number % 2 === 0;
			    // JavaScript is, however, zero-based, so want those elements with a modulo of 1:
			    return index % 2 === 1;
			  });
			  //finalList.push(filteredData);
			  //filteredData = [];
			  }
		
			/**for(var i = 0; i < csvOutput.length; i++){
				for (var u = 0; u < csvOutput[i].length; u++){
				    if(u % 2 === 0){
				        csvOutput[i].splice(u, 1);
				    	}
				    if(i == index && u & 2 === 0){
				    	headerCsv.push(csvOutput[i]);
				        csvOutput.splice(i, 1);
				    	}
		    	}
			}**/
			filteredData.unshift(filteredName);
			


			//console.log(csvOutput);
			return output[x];
			//console.log(x);
			//x = x + 1;
			//return null;
			
        	
	//i = i + 1;
        
        },
    }
    /**{
        Header: 'Books',
        id:'books',
        accessor: d => {
            let output = [];
            _.map(d.b, book => {
                output.push(book.title);
            });
            return output.join(', ');
        },
    }**/


		/**, {
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
	}**/]
	
    return (

			<div>
				{hist.items &&
					<ReactTable style={{"width": "100%"}} className="-striped -highlight"
						data={hist.items}
						columns={columns}
						filterable={true}
					/>
				}
			</div>	
    );
  }
}

function mapStateToProps(state) {
    const { full, hist, users, authentication } = state;
    const { user } = authentication;
    return {
        user,
        users,
        hist,
        full
    };
}

const connectedHistoryPage = connect(mapStateToProps)(HistoryPage);
export { connectedHistoryPage as HistoryPage };
