<template>
  <!-- Outer wrapper centers the form on the page -->
  <div class="login-container">
      <div class="login-card">
        <h1>SupplyFlowApp</h1>
        <h2>Please Log in</h2>

        <!-- Login form — @submit.prevent stops the browser from reloading the page -->
        <form @submit.prevent="handleLogin">

          <div>
            <label>Username</label>
            <!-- v-model links the input field to the 'username' variable (two-way binding) -->
            <input v-model="username" type="text" placeholder="Enter username" required />
          </div>

          <div>
            <label>Password</label>
            <!-- v-model links the input field to the 'password' variable -->
            <input v-model="password" type="password" placeholder="Enter password" required />
          </div>

          <!-- v-if renders this element only when 'errorMessage' is not empty -->
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

          <button type="submit">Log in</button>

        </form>
        <!-- Link to registration page -->
        <p class="switch-link">
          Don't have an account?
        <router-link to="/register">Register</router-link>
      </p>
      </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

// ref() creates a reactive variable — when it changes, the template updates automatically
const username = ref('')
const password = ref('')
const errorMessage = ref('')

// useRouter() gives us access to the router so we can navigate programmatically
const router = useRouter()

async function handleLogin() {
  // Reset the error message on every new attempt
  errorMessage.value = ''

  try {
    // POST credentials to Django's JWT endpoint
    // axios automatically converts the object to JSON
    const response = await api.post('/token/', {
      username: username.value,
      password: password.value,
    })

    // Django returns both tokens — store them in browser localStorage
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // Fetch current user data and store it — needed for ticket filtering
    const userResponse = await api.get('/me')
    localStorage.setItem('current_user', JSON.stringify(userResponse.data))

    // Navigate to the tickets page after successful login
    router.push('/tickets')

  } catch (error) {
    // If Django returns 401 (wrong credentials), show a message to the user
    errorMessage.value = 'Invalid username or password.'
  }
}
</script>

<style scoped>
/*Poppins font to the whole container */
  .login-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #667eea 0%, #c850c0 60%, #ff6eb4 100%);
    font-family: 'Poppins', sans-serif;
  }

  /* White card in the center */
  .login-card {
    background: white;
    padding: 2.5rem 2rem;
    border-radius: 24px;
    width: 100%;
    max-width: 360px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  h1 {
    font-size: 2rem;
    color: #5b21b6;
    margin-bottom: 0.25rem;
  }

  h2 {
    font-size: rem;
    color: #888;
    font-weight: 400;
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    text-align: left;
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 0.3rem;
  }

  input {
    display: block;
    width: 100%;
    margin-bottom: 1.2rem;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border: 1.5px solid #e5e7eb;
    border-radius: 12px;
    outline: none;
    box-sizing: border-box;
    transition: border-color 0.2s;
  }

  /* Highlight the input border when user clicks on it */
  input:focus {
    border-color: #667eea;
  }

  /* Gradient button matching the background */
  button {
    width: 100%;
    padding: 0.85rem;
    background: linear-gradient(135deg, #667eea, #c850c0);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
  }

  button:hover {
    opacity: 0.9;
  }

  .error {
    color: #dc2626;
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }

  .switch-link { margin-top: 1.2rem; font-size: 0.9rem; color: #666; }
  .switch-link a { color: #667eea; font-weight: 600; text-decoration: none; }

  /* Keyframe animation — defines the motion from start to end */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);  /* starts 40px lower */
  }
  to {
    opacity: 1;
    transform: translateY(0);     /* ends at normal position */
  }
}

/* Applying the animation to the card */
.login-card {
  animation: slideUp 1s ease-out;
}
</style>
