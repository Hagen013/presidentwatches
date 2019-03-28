import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '../store'
import { getToken } from '@/utils/auth'


const service = axios.create({
  baseURL: "http://localhost:8000/api/v0",
  timeout: 5000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  }
})

service.interceptors.request.use(
  config => {
    if (store.getters.token) {
      config.headers['x-token'] = getToken();
    }
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
    return Promise.reject(error)
  }
)

export default service
