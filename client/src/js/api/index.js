import axios from 'axios'
import csrfToken from '@/utils/csrfToken'

const service = axios.create({
    baseURL: "/api/v0",
    timeout: 5000,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken()
    }
})

export default service