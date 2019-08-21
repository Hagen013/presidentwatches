import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '../store'
import { getToken } from '@/utils/auth'
import baseURL from '@/utils/baseUrl'


const service = axios.create({
  baseURL: baseURL,
  timeout: 50000,
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

    if ( (error.response.code === 401) || (error.response.code == 403) ) {
      store.dispatch('user/logout').then(() => {
        location.reload()
      })
    } else {
      Message({
        message: error.message,
        type: 'error',
        duration: 5 * 1000
      })
    }
    return Promise.reject(error);

  }

)

export default service
