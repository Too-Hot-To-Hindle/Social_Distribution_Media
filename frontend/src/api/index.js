import axios from 'axios'
import { csrftoken } from './csrftoken';

// const BASE_URL = 'http://127.0.0.1:8000'
const BASE_URL = (process.env.NODE_ENV === 'production') ? 'https://social-distribution-media.herokuapp.com' : 'http://127.0.0.1:8000'

export const ENDPOINTS = {
    authors: 'authors',
    authorsAuth: 'auth',
    csrf: 'csrf'
}

export const createAPIEndpoint = endpoint => {
    let url = BASE_URL + '/api/' + endpoint
    const requestOptions = {
        headers: authHeader(),
        credentials: "same-origin"
    }

    return {
        post: data => axios.post(url, data, requestOptions),
        get: () => axios.get(url, requestOptions),
        delete: () => axios.delete(url, requestOptions),
    }
}

function authHeader() {
    // return authorization header with basic auth credentials
    let authData = localStorage.getItem('authData');
    if (authData) {
        return { 
            // 'Authorization': 'Basic ' + authData,
            // 'X-CSRFToken': csrftoken
        };
    } else {
        return {
            'X-CSRFToken': csrftoken
        };
    }
}