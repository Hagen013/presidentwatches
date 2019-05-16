import axios from 'axios'

const service = axios.create({
    baseURL: GEO_SERVICE_HOST,
    timeout: 5000,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
})

export default service;