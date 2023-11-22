import axios from "axios";
import cookie from 'js-cookie';

function isAuthNeed(endpoint) {
    return endpoint !== 'login' && endpoint !== 'register'
}

export default function Api() {

    const BASEURL = 'http://localhost:8000/';

    return {
        Get: (url, params = {}) => {

            let __headers = {}

            __headers['accept'] = 'application/json';
            __headers['Content-Type'] = 'application/json';

            if (isAuthNeed(url)) {
                let authInfo = JSON.parse(cookie.get("IOT_APP_AUTH") || "{}");

                if (!authInfo['access_token']) {
                    window.location = '/login';
                }
                __headers['Authorization'] = authInfo['token_type'] + ' ' + authInfo['access_token'];
            }

            return axios.get(BASEURL + url, {
                headers: __headers,
                params: typeof params == 'string' ? JSON.parse(params) : params
            })
        },

        Post: (url, params = {}) => {
            let __headers = {}

            __headers['accept'] = 'application/json';
            __headers['Content-Type'] = 'application/json';

            if (isAuthNeed(url)) {
                let authInfo = JSON.parse(cookie.get("IOT_APP_AUTH") || "{}");

                if (!authInfo['access_token']) {
                    window.location = '/login';
                }
                __headers['Authorization'] = authInfo['token_type'] + ' ' + authInfo['access_token'];
            }

            return axios.post(BASEURL + url, typeof params == 'string' ? JSON.parse(params) : params, {
                headers: __headers
            })
        }
    }
}