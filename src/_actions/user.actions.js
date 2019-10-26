/**
 * Redux action creators for actions a user can take in the application
 * 
 *
 * @author Nathan Fallowfield.
 * @since  1.0.0
 */
 
import { userConstants } from '../_constants';
import { userService } from '../_services';
import { alertActions } from './';
import { history } from '../_helpers';

// Public user actions are exposed via userActions
export const userActions = {
	login,
	logout,
	register,
	getAll,
	submit,
	submitImage,
	getHistory,
	getImages,
	delete: _delete
};

//Dispatch a login request
function login(username, password) {
	return dispatch => {
		dispatch(request({ username }));

		userService.login(username, password)
			.then(
				user => { 
					dispatch(success(user));
					history.push('/');
				},
				error => {
					dispatch(failure(error.toString()));
					dispatch(alertActions.error(error.toString()));
                }
			);
	};

	function request(user) { return { type: userConstants.LOGIN_REQUEST, user } }
	function success(user) { return { type: userConstants.LOGIN_SUCCESS, user } }
	function failure(error) { return { type: userConstants.LOGIN_FAILURE, error } }
}

//Dispatch a login request
function logout() {
	userService.logout();
	return { type: userConstants.LOGOUT };
}

//Dispatch a register user request
function register(user) {
	return dispatch => {
		dispatch(request(user));

		userService.register(user)
			.then(
				user => { 
					dispatch(success());
					history.push('/login');
					dispatch(alertActions.success('Registration successful'));
				},
				error => {
					dispatch(failure(error.toString()));
					dispatch(alertActions.error(error.toString()));
				}
			);
	};

	function request(user) { return { type: userConstants.REGISTER_REQUEST, user } }
	function success(user) { return { type: userConstants.REGISTER_SUCCESS, user } }
	function failure(error) { return { type: userConstants.REGISTER_FAILURE, error } }
}

// Dispatch a request to get all users
function getAll() {
	return dispatch => {
		dispatch(request());

		userService.getAll()
			.then(
				users => dispatch(success(users)),
				error => dispatch(failure(error.toString()))
			);
	};

	function request() { return { type: userConstants.GETALL_REQUEST } }
	function success(users) { return { type: userConstants.GETALL_SUCCESS, users } }
	function failure(error) { return { type: userConstants.GETALL_FAILURE, error } }
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
	return dispatch => {
		dispatch(request(id));

		userService.delete(id)
			.then(
				user => dispatch(success(id)),
				error => dispatch(failure(id, error.toString()))
			);
	};

	function request(id) { return { type: userConstants.DELETE_REQUEST, id } }
	function success(id) { return { type: userConstants.DELETE_SUCCESS, id } }
	function failure(id, error) { return { type: userConstants.DELETE_FAILURE, id, error } }
}


// Dispatch a request to save data a user has input
function submit(id, loc, size, conditions, date, imageURL, lat, lng, species, common) {
	return dispatch => {
		userService.saveData(id, loc, size, conditions, date, imageURL, lat, lng, species, common)
			.then(
				response => { 
					dispatch(alertActions.success('Submitted Data'));
				},
				error => {
					dispatch(alertActions.error(error.toString()));
				}
			);
	};
}

// Dispatch a save image request
function submitImage(file, filename) {
	return dispatch => {
		userService.saveImage(file, filename)
			.then(
				response => { 
					dispatch(alertActions.success('Submitted Data'));
				},
				error => {
					dispatch(alertActions.error(error.toString()));
				}
			);
	};
}

// Dispatch a request to retrive a users data submission history
function getHistory() {
	return dispatch => {
		dispatch(request());
		dispatch(alertActions.clear());
		
		userService.getUsersData()
			.then(
				response => { 
					dispatch(success(response));
				},
				error => {
					dispatch(failure(error.toString()));
				}
			);
	};
    
	function request() { return { type: userConstants.GETHIST_REQUEST } }
	function success(res) { return { type: userConstants.GETHIST_SUCCESS, res } }
	function failure(error) { return { type: userConstants.GETHIST_FAILURE, error } }
}


// Dispatch a request to retrive a users images
function getImages() {
	return dispatch => {
		dispatch(request());
		dispatch(alertActions.clear());
		
		userService.getImages()
			.then(
				response => { 
					dispatch(success(response));
				},
				error => {
					dispatch(failure(error.toString()));
				}
			);
	};
    
	function request() { return { type: userConstants.GETIMAGES_REQUEST } }
	function success(res) { return { type: userConstants.GETIMAGES_SUCCESS, res } }
	function failure(error) { return { type: userConstants.GETIMAGES_FAILURE, error } }
}
