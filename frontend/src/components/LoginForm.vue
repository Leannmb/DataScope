<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  isLoading: boolean
  errorMessage: string
}>()

const emit = defineEmits<{
  login: [email: string, password: string]
  showRegister: []
}>()

const email = ref('')
const password = ref('')

function submitForm(): void {
  emit(
    'login',
    email.value,
    password.value,
  )
}
</script>

<template>
  <section>
    <h2>Iniciar sesión</h2>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="login-email">
          Correo electrónico
        </label>

        <input
          id="login-email"
          v-model.trim="email"
          type="email"
          autocomplete="email"
          required
        >
      </div>

      <div class="form-group">
        <label for="login-password">
          Contraseña
        </label>

        <input
          id="login-password"
          v-model="password"
          type="password"
          autocomplete="current-password"
          required
        >
      </div>

      <p v-if="errorMessage">
        Error: {{ errorMessage }}
      </p>

      <button
        type="submit"
        :disabled="isLoading"
      >
        {{ isLoading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
      </button>
    </form>

    <p>
      ¿No tienes una cuenta?

      <button
        type="button"
        @click="emit('showRegister')"
      >
        Registrarse
      </button>
    </p>
  </section>
</template>