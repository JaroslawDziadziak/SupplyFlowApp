import axios from 'axios'

// Create a pre-configured axios instance
// Instead of writing the full URL every time, we set a base here once
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})

// Interceptor: a function that runs automatically before EVERY request
// Think of it as a checkpoint — it attaches the token to every outgoing call
api.interceptors.request.use((config) => {

  // Read the access token from browser storage
  const token = localStorage.getItem('access_token')

  if (token) {
    // Django's JWT middleware looks for exactly this format: "Bearer <token>"
    config.headers.Authorization = `Bearer ${token}`
  }

  // Must return config — axios needs it to continue sending the request
  return config
})

export default api
