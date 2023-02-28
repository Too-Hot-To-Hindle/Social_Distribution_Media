import axios from 'axios'

// const BASE_URL = 'http://127.0.0.1:8000/'
const BASE_URL = 'https://social-distribution-media.herokuapp.com/'

export const ENDPOINTS = {
    createAuthor: 'author/create'
}

export const createAPIEndpoint = endpoint => {
    let url = BASE_URL + '/api/' + endpoint + '/'
    const requestOptions = {
        headers: authHeader()
    }
    // console.log(JSON.stringify(requestOptions));
    return {
        post: data => axios.post(url, data, requestOptions),
        get: () => axios.get(url, requestOptions)
    }
}

function authHeader() {
    // return authorization header with basic auth credentials
    let authData = localStorage.getItem('authData');
    if (authData) {
        return { 'Authorization': 'Basic ' + authData };
    } else {
        return {};
    }
}