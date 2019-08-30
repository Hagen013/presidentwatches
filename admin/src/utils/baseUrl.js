
let baseURL = 'https://presidentwatches.ru/api/v0'

if (process.env.NODE_ENV === 'development') {
  baseURL = 'http://localhost:8000/api/v0'
}

export default baseURL