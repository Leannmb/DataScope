<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  isLoading: boolean
  errorMessage: string
}>()

const emit = defineEmits<{
  register: [
    name: string,
    email: string,
    password: string,
  ]
  showLogin: []
}>()

const name = ref('')
const email = ref('')
const password = ref('')

function submitForm(): void {
  emit(
    'register',
    name.value,
    email.value,
    password.value,
  )
}
</script>

<template>
  <section>
    <h2>Crear una cuenta</h2>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="register-name">
          Nombre
        </label>

        <input
          id="register-name"
          v-model.trim="name"
          type="text"
          autocomplete="name"
          required
        >
      </div>

      <div class="form-group">
        <label for="register-email">
          Correo electrónico
        </label>

        <input
          id="register-email"
          v-model.trim="email"
          type="email"
          autocomplete="email"
          required
        >
      </div>

      <div class="form-group">
        <label for="register-password">
          Contraseña
        </label>

        <input
          id="register-password"
          v-model="password"
          type="password"
          autocomplete="new-password"
          minlength="8"
          maxlength="72"
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
        {{ isLoading ? 'Creando cuenta...' : 'Registrarse' }}
      </button>
    </form>

    <p>
      ¿Ya tienes una cuenta?

      <button
        type="button"
        @click="emit('showLogin')"
      >
        Iniciar sesión
      </button>
    </p>
  </section>
</template>