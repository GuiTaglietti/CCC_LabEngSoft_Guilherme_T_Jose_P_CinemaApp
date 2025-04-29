<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">Fazer login</h2>

      <div class="form-group mb-4">
        <el-input
          v-model="username"
          placeholder="Email ou nome de usuário"
          class="login-input"
          clearable
        >
          <template #prefix>
            <i class="bi bi-person-fill text-danger"></i>
          </template>
        </el-input>
      </div>

      <div class="form-group mb-4">
        <el-input
          v-model="password"
          type="password"
          placeholder="Senha"
          class="login-input"
          show-password
        >
          <template #prefix>
            <i class="bi bi-lock-fill text-danger"></i>
          </template>
        </el-input>
      </div>

      <div
        class="d-flex justify-content-between align-items-center text-white mb-3"
      >
        <el-checkbox v-model="rememberMe" class="remember"
          >Lembrar sessão</el-checkbox
        >
        <a href="#" class="forgot" @click="goToForgotPassword"
          >Esqueci a senha</a
        >
      </div>

      <el-button type="danger" class="login-button w-100" @click="submit">
        <i class="bi bi-box-arrow-in-right me-2"></i> Entrar
      </el-button>

      <p v-if="error" class="login-error mt-3">{{ error }}</p>

      <p class="signup-text mt-4">
        Não tem uma conta?
        <router-link to="/register" class="signup-link"
          >Cadastrar-se</router-link
        >
      </p>
    </el-card>
  </div>
</template>

<script>
import { ref } from "vue";
import { login } from "../services/auth";
import { useRouter } from "vue-router";
import { useSessionStore } from "../store/session";

export default {
  setup() {
    const router = useRouter();
    const sessionStore = useSessionStore();

    const username = ref("");
    const password = ref("");
    const error = ref("");
    const rememberMe = ref(false);

    const submit = async () => {
      try {
        const { access_token } = await login(username.value, password.value);
        sessionStore.setSession(access_token);

        if (rememberMe.value) {
          localStorage.setItem("access_token", access_token);
        }

        if (sessionStore.role === "gerente") {
          router.push("/gerente");
        } else {
          router.push("/usuario");
        }
      } catch (e) {
        error.value = "Login inválido";
      }
    };

    const goToForgotPassword = () => {
      router.push("/forgot-password");
    };

    return {
      username,
      password,
      submit,
      error,
      rememberMe,
      goToForgotPassword,
    };
  },
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.login-container {
  min-height: 100vh;
  background-color: #0d0d0d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.login-card {
  background-color: #1a1a1a;
  border: none;
  box-shadow: 0 0 25px red;
  border-radius: 1rem;
  padding: 2.5rem;
  max-width: 420px;
  width: 100%;
}

.login-title {
  text-align: center;
  font-size: 2rem;
  color: #fff;
  margin-bottom: 1.5rem;
}

.login-input :deep(.el-input__wrapper) {
  background-color: #111;
  border: 1px solid #ff0000;
  color: #fff;
  padding: 0.4rem 0.75rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease-in-out;
}

.login-input :deep(.el-input__inner) {
  color: #fff;
}

.login-button {
  background-color: #ff0000;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 10px red;
}

.login-button:hover {
  box-shadow: 0 0 20px red;
}

.login-error {
  color: red;
  text-align: center;
}

.forgot {
  color: red;
  text-decoration: none;
  font-size: 0.85rem;
}

.signup-text {
  color: white;
  text-align: center;
  font-size: 0.9rem;
}

.signup-link {
  color: red;
  text-decoration: none;
  font-weight: bold;
}

.remember :deep(.el-checkbox__label) {
  color: white;
}
</style>
