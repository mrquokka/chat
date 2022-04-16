import axios from 'axios'

# Full config:  https://github.com/axios/axios#request-config
# axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
# axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
# axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

_axios = axios.create({
  # baseURL: process.env.baseURL || process.env.apiUrl || ""
  # timeout: 60 * 1000, # Timeout
  withCredentials: true
})

setTimeout(() ->
  socket = new WebSocket("ws://127.0.0.1:5000/")
)


export default {
  send_query: (data) ->
    console.log data
    return _axios.post('/api', data).then()
}
