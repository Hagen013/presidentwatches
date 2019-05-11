import axios from 'axios'

const service = axios.create({
    baseURL: "http://127.0.0.1:8282",
    timeout: 5000,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
})

export default service;