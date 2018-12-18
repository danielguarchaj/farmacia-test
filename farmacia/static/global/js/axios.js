axios = axios.create({
    baseURL: '/api/',
    headers: {
        'Content-Type': 'application/json'
    }
})

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'