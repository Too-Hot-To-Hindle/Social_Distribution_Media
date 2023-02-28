import React from 'react';
import Cookies from 'js-cookie';

/**
 * https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
 * https://www.stackhawk.com/blog/django-csrf-protection-guide/#using-react-forms-to-render-a-csrf-token
 */

export const csrftoken = Cookies.get('csrftoken');

const CSRFTOKEN = () => {
    return (
        <input name="csrfmiddlewaretoken" value={csrftoken} type="hidden" />
    );
};

export default CSRFTOKEN;