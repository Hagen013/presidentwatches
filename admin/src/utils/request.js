import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '../store'
import { getToken } from '@/utils/auth'

console.log('tsoy')
console.log(process.env)
if (process.env.NODE_ENV === 'development') {
  const baseURL = 'http://localhost:8000/api/v0'
} else {
  const baseURL = 'http://http://5.189.227.162/api/v0'
}

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
    if (store.getters.token) {
      let token = getToken()
      config.headers.common['Authorization'] = `Bearer ${token}`;
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
