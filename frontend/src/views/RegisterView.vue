<template>
  <div class="register-container">
    <div class="register-card">
      <h1>SupplyFlow</h1>
      <h2>Create account</h2>

      <form @submit.prevent="handleRegister">

        <label>Username</label>
        <input v-model="username" type="text" placeholder="Enter username" required />

        <label>Email</label>
        <input v-model="email" type="email" placeholder="Enter email" />

        <label>Password</label>
        <input v-model="password" type="password" placeholder="Min. 8 characters" required />

        <label>Role</label>
        <!-- v-model on a <select> works the same as on <input> -->
        <select v-model="role" required>
          <option value="logistics">Logistics</option>
          <option value="project_manager">Project Manager</option>
          <option value="engineer">Engineer</option>
          <option value="other">Other</option>
        </select>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>

        <button type="submit">Register</button>

      </form>

      <!-- Link back to login page -->
      <p class="switch-link">
        Already have an account?
        <!-- router-link renders as <a> but navigates without page reload -->
        <router-link to="/login">Log in</router-link>
      </p>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const role = ref('logistics')       // default selected option
const errorMessage = ref('')
const successMessage = ref('')

async function handleRegister() {
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // POST to Django's /api/register/ endpoint
    await api.post('/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      role: role.value,
    })

    // Show success and redirect to login after 1.5 seconds
    successMessage.value = 'Account created! Redirecting to login...'
    setTimeout(() => router.push('/login'), 1500)

  } catch (error) {
    // Django returns field-level errors e.g. { username: ["Already exists"] }
    const data = error.response?.data
    if (data) {
      // Extract first error message from whatever field failed
      const firstError = Object.values(data)[0]
      errorMessage.value = Array.isArray(firstError) ? firstError[0] : firstError
    } else {
      errorMessage.value = 'Registration failed. Please try again.'
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #c850c0 60%, #ff6eb4 100%);
  font-family: 'Poppins', sans-serif;
}

.register-card {
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 24px;
  width: 100%;
  max-width: 380px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  text-align: center;
  animation: slideUp 0.6s ease-out;
}

h1 { font-size: 2rem; font-weight: 700; color: #5b21b6; margin-bottom: 0.25rem; }
h2 { font-size: 1rem; color: #888; font-weight: 400; margin-bottom: 1.5rem; }

label {
  display: block;
  text-align: left;
  font-size: 0.9rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.3rem;
}

input, select {
  display: block;
  width: 100%;
  margin-bottom: 1.2rem;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-family: 'Poppins', sans-serif;
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus, select:focus { border-color: #667eea; }

button {
  width: 100%;
  padding: 0.85rem;
  background: linear-gradient(135deg, #667eea, #c850c0);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  margin-top: 0.5rem;
}

button:hover { opacity: 0.9; }

.error { color: #dc2626; font-size: 0.9rem; margin-bottom: 0.5rem; }
.success { color: #16a34a; font-size: 0.9rem; margin-bottom: 0.5rem; }

.switch-link { margin-top: 1.2rem; font-size: 0.9rem; color: #666; }
.switch-link a { color: #667eea; font-weight: 600; text-decoration: none; }

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
