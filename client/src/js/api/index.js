import axios from 'axios'

const service = axios.create({
    baseURL: "/api/v0",
    timeout: 5000,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
})

export default service;