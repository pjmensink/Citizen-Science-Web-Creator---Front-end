/**
 * Redux action creators for actions related to alerts within the application
 *
 * @author Nathan Fallowfield.
 * @since  1.0.0
 */
 
import { alertConstants } from '../_constants';

export const alertActions = {
	success,
	error,
	clear
};

function success(message) {
	return { type: alertConstants.SUCCESS, message };
}

function error(message) {
	return { type: alertConstants.ERROR, message };
}

function clear() {
	return { type: alertConstants.CLEAR };
}
