import React from 'react';
import Cookies from 'js-cookie';

/**
 * https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
 * https://www.stackhawk.com/blog/django-csrf-protection-guide/#using-react-forms-to-render-a-csrf-token
 */

export const csrftoken = Cookies.get('csrftoken');

// export const csrftoken = createAPIEndpoint(ENDPOINTS.csrf).get().then((resp) => console.log(resp)).catch((err) => console.log(err))

const CSRFTOKEN = () => {
    return (
        <input name="csrfmiddlewaretoken" value={csrftoken} type="hidden" />
    );
};

export default CSRFTOKEN;