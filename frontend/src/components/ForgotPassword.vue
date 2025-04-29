<template>
    <div class="login-container">
      <el-card class="login-card">
        <h2 class="login-title">Recuperar senha</h2>
  
        <div class="form-group mb-4">
          <el-input
            v-model="email"
            placeholder="Email ou nome de usuário"
            class="login-input"
            clearable
          >
            <template #prefix>
              <i class="bi bi-person-fill text-danger"></i>
            </template>
          </el-input>
        </div>
  
        <el-button type="danger" class="login-button w-100" @click="submit">
          <i class="bi bi-arrow-repeat me-2"></i> Recuperar senha
        </el-button>
  
        <p v-if="error" class="login-error mt-3">{{ error }}</p>
  
        <p class="signup-text mt-4">
          Lembrou a senha?
          <router-link to="/login" class="signup-link"
            >Voltar para login</router-link
          >
        </p>
      </el-card>
    </div>
  
    <!-- Caixa de diálogo de sucesso -->
    <el-dialog
      v-model="dialogVisible"
      title="Sucesso"
      :close-on-click-modal="false"
      :show-close="false"
      class="success-dialog"
    >
      <span>Solicitação de recuperação de senha enviada com sucesso! Confira seu e-mail.</span>
      <template #footer>
        <el-button
          type="primary"
          class="dialog-button"
          @click="redirectToLogin"
        >
          Voltar para login
        </el-button>
      </template>
    </el-dialog>
  </template>
  
  <script>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { recoverPassword } from "../services/auth"; // Importe o serviço de recuperação de senha
  
  export default {
    setup() {
      const router = useRouter();
      const email = ref("");
      const error = ref("");
      const dialogVisible = ref(false);
  
      const submit = async () => {
        try {
          const response = await recoverPassword(email.value); // Chama o serviço de recuperação
          dialogVisible.value = true; // Exibe a caixa de diálogo de sucesso
        } catch (e) {
          error.value = "Erro ao enviar solicitação. Tente novamente.";
        }
      };
  
      const redirectToLogin = () => {
        router.push("/login"); // Redireciona para a tela de login
      };
  
      return { email, submit, error, dialogVisible, redirectToLogin };
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
  
  /* Estilo da caixa de diálogo */
  .success-dialog .el-dialog__header {
    background-color: #1a1a1a;
    color: #fff;
    border-bottom: 2px solid #ff0000;
  }
  
  .success-dialog .el-dialog__body {
    color: #fff;
    font-size: 1rem;
    padding: 20px;
  }
  
  .success-dialog .dialog-button {
    background-color: #ff0000;
    color: white;
    font-weight: bold;
    border-radius: 0.5rem;
    padding: 0.75rem;
    transition: box-shadow 0.3s ease;
    box-shadow: 0 0 10px red;
  }
  
  .success-dialog .dialog-button:hover {
    box-shadow: 0 0 20px red;
  }
  </style>
  