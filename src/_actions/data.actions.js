/**
 * Redux action creators for actions related to data submission and retrieval
 *
 * @author Nathan Fallowfield.
 * @since  1.0.0
 */
 
export const dataActions = {
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
