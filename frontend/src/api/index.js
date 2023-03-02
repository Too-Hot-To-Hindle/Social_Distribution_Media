import axios from 'axios'
import Cookies from 'js-cookie'
import { csrftoken } from './csrftoken';

const BASE_URL = 'http://127.0.0.1:8000'
// const BASE_URL = 'https://social-distribution-media.herokuapp.com'

export const BASIC_AUTH_COOKIE_NAME = 'X-SOCIAL-DISTRIBUTION-BASIC-AUTH';

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
        get: () => axios.get(url, requestOptions)
    }
}

function authHeader() {
    // return authorization header with basic auth credentials
    let authData = Cookies.get(BASIC_AUTH_COOKIE_NAME);
    if (authData) {
        return { 
            'Authorization': 'Basic ' + authData,
            'X-CSRFToken': csrftoken
        };
    } else {
        return {
            'X-CSRFToken': csrftoken
        };
    }
}