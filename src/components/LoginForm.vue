<template>
  <div>
    <h2>Login</h2>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="submit">Login</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import { ref } from 'vue';
import { login } from '../services/auth';
import { useRouter } from 'vue-router';
import { useSessionStore } from '../store/session';

export default {
  setup() {
    const router = useRouter();
    const sessionStore = useSessionStore();

    const username = ref('');
    const password = ref('');
    const error = ref('');

    const submit = async () => {
      try {
        const { access_token } = await login(username.value, password.value);
        sessionStore.setSession(access_token);

        console.log('sessionstore: ', sessionStore)

        if (sessionStore.role === 'gerente') {
          router.push('/gerente');
        } else {
          router.push('/usuario');
        }
      } catch (e) {
        error.value = 'Login inválido';
      }
    };

    return { username, password, submit, error };
  },
};
</script>
