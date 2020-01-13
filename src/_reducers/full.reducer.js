import { userConstants } from '../_constants';

export function full(state = {}, action) {
  switch (action.type) {
    case userConstants.GETITEM_REQUEST:
      return {
        loading: true
      };
    case userConstants.GETITEM_SUCCESS:
      return {
        items: action.res
      };
    case userConstants.GETITEM_FAILURE:
      return { 
        error: action.error
      };
    default:
      return state
  }
}

