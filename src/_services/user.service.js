import config from 'config';
import { authHeader } from '../_helpers';

export const userService = {
    login,
    logout,
    register,
    getAll,
    getById,
    update,
    saveData,
    saveImage,
    getUsersData,
    getAllItems,
    getImages,
    delete: _delete
};

function login(username, password) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    };

    return fetch(`${config.apiUrl}/users/authenticate`, requestOptions)
        .then(handleResponse)
        .then(user => {
            // login successful if there's a jwt token in the response
            if (user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }

            return user;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

function getAll() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse);
}


function getById(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users/${id}`, requestOptions).then(handleResponse);
}

function register(user) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
    };

    return fetch(`${config.apiUrl}/users/register`, requestOptions).then(handleResponse);
}

function update(user) {
    const requestOptions = {
        method: 'PUT',
        headers: { ...authHeader(), 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
    };

    return fetch(`${config.apiUrl}/users/${user.id}`, requestOptions).then(handleResponse);;
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
    const requestOptions = {
        method: 'DELETE',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users/${id}`, requestOptions).then(handleResponse);
}

function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                window.location.reload(true);
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}

function saveData(data) {
	const user = localStorage.getItem('user');
	const userId = JSON.parse(user)._id;
	const requestOptions = {
        method: 'POST',
        headers: { ...authHeader(), 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, data })
        //body: JSON.stringify({ userId, model })
    };
    return fetch(`${config.apiUrl}/fishdata/submit`, requestOptions).then(handleResponse);
}

function saveImage(file, filename) {
	
	const data = new FormData();
    data.append('file', file);
    data.append('filename', filename);
	const requestOptions = {
        method: 'POST',
        headers: { ...authHeader() },
        body: data
    };
    
    return fetch(`${config.apiUrl}/upload`, requestOptions).then(handleResponse);
}

function getUsersData() {
    const user = localStorage.getItem('user');
	const userId = JSON.parse(user)._id
	
	const requestOptions = {
        method: 'POST',
        headers: { ...authHeader(), 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId })
    };
    
    return fetch(`${config.apiUrl}/fishdata/getAll`, requestOptions).then(handleResponse);
}

function getAllItems() {
    
    const requestOptions = {
        //method: 'GET',
        //headers: authHeader(),
        method: 'POST',
        headers: { ...authHeader(), 'Content-Type': 'application/json' }
        //body: JSON.stringify({})
    };
    
    return fetch(`${config.apiUrl}/fishdata/getAllItems`, requestOptions).then(handleResponse);
}

function getImages() {
	const user = localStorage.getItem('user');
	const userId = JSON.parse(user)._id
	
	const requestOptions = {
        method: 'GET',
        headers: { ...authHeader()},
    };
    
    return fetch(`${config.apiUrl}/fish.jpg`, requestOptions).then(handleImageResponse);
}

function handleImageResponse(response) {
    return response.blob().then(blob => {
        var data = URL.createObjectURL(blob);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                window.location.reload(true);
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}
