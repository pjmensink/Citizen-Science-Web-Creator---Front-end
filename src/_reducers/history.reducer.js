import { userConstants } from '../_constants';

export function hist(state = {}, action) {
  switch (action.type) {
    case userConstants.GETHIST_REQUEST:
      return {
        loading: true
      };
    case userConstants.GETHIST_SUCCESS:
      return {
        items: action.res
      };
    case userConstants.HIST_FAILURE:
      return { 
        error: action.error
      };
    default:
      return state
  }
}

