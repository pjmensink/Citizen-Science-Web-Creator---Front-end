import { userConstants } from '../_constants';

export function images(state = {}, action) {
  switch (action.type) {
    case userConstants.GETIMAGES_REQUEST:
      return {
        loading: true
      };
    case userConstants.GETIMAGES_SUCCESS:
      return {
        items: action.res
      };
    case userConstants.GETIMAGES_FAILURE:
      return { 
        error: action.error
      };
    default:
      return state
  }
}

