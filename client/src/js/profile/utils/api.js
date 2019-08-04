import axios from 'axios'
import baseURL from '../utils/baseUrl'


const service = axios.create({
  baseURL: baseURL,
  timeout: 5000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  }
})

service.interceptors.request.use(
  config => {
    return config
  },
  error => {
    Promise.reject(error)
  }
)


service.interceptors.response.use(

  response => {

    return response

  },
  error => {
    return Promise.reject(error);
  }

)

export default service
