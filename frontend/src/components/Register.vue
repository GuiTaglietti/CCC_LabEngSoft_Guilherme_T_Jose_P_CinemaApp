<template>
    <div class="register-container">
      <el-card class="register-card">
        <h2 class="register-title">Cadastre-se</h2>
  
        <div class="form-group mb-3">
          <el-input
            v-model="form.fullname"
            placeholder="Nome completo"
            class="register-input"
            clearable
          >
            <template #prefix>
              <i class="bi bi-person-fill text-danger"></i>
            </template>
          </el-input>
        </div>
  
        <div class="form-group mb-3">
          <el-input
            v-model="form.cpf"
            placeholder="CPF"
            class="register-input"
            clearable
          >
            <template #prefix>
              <i class="bi bi-card-text text-danger"></i>
            </template>
          </el-input>
        </div>
  
        <div class="form-group mb-3">
          <el-input
            v-model="form.email"
            placeholder="Email"
            class="register-input"
            clearable
          >
            <template #prefix>
              <i class="bi bi-envelope-fill text-danger"></i>
            </template>
          </el-input>
        </div>
  
        <div class="form-group mb-3">
          <el-input
            v-model="form.confirmEmail"
            placeholder="Confirmar email"
            class="register-input"
            clearable
          >
            <template #prefix>
              <i class="bi bi-envelope-check-fill text-danger"></i>
            </template>
          </el-input>
        </div>
  
        <div class="form-group mb-3">
          <el-input
            v-model="form.username"
            placeholder="Nome de usuário"
            class="register-input"
            clearable
          >
            <template #prefix>
              <i class="bi bi-person-badge-fill text-danger"></i>
            </template>
          </el-input>
        </div>
  
        <div class="form-group mb-4">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Senha"
            show-password
            class="register-input"
          >
            <template #prefix>
              <i class="bi bi-lock-fill text-danger"></i>
            </template>
          </el-input>
        </div>
  
        <el-button type="danger" class="register-button w-100" @click="submit">
          <i class="bi bi-person-plus-fill me-2"></i> Criar cadastro
        </el-button>
  
        <p v-if="error" class="register-error mt-3">{{ error }}</p>
        <p v-if="success" class="register-success mt-3">{{ success }}</p>
  
        <p class="login-text mt-4">
          Já tem uma conta?
          <router-link to="/login" class="login-link">Fazer login</router-link>
        </p>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { register } from "../services/auth";
  
  const form = ref({
    fullname: "",
    cpf: "",
    email: "",
    confirmEmail: "",
    username: "",
    password: "",
  });
  
  const error = ref("");
  const success = ref("");
  const router = useRouter();
  
  const submit = async () => {
    error.value = "";
    success.value = "";
  
    try {
      const response = await register(form.value);
      success.value = response.msg || "Cadastro realizado com sucesso!";
      setTimeout(() => router.push("/login"), 1500);
    } catch (errMsg) {
      error.value = errMsg;
    }
  };
  </script>
  
  <style scoped>
  @import "bootstrap-icons/font/bootstrap-icons.css";
  
  .register-container {
    min-height: 100vh;
    background-color: #0d0d0d;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .register-card {
    background-color: #1a1a1a;
    border: none;
    box-shadow: 0 0 25px red;
    border-radius: 1rem;
    padding: 2.5rem;
    max-width: 500px;
    width: 100%;
  }
  
  .register-title {
    text-align: center;
    font-size: 2rem;
    color: #fff;
    margin-bottom: 1.5rem;
  }
  
  .register-input :deep(.el-input__wrapper) {
    background-color: #111;
    border: 1px solid #ff0000;
    color: #fff;
    padding: 0.4rem 0.75rem;
    border-radius: 0.5rem;
    transition: all 0.3s ease-in-out;
  }
  
  .register-input :deep(.el-input__inner) {
    color: #fff;
  }
  
  .register-button {
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
  
  .register-button:hover {
    box-shadow: 0 0 20px red;
  }
  
  .register-error {
    color: red;
    text-align: center;
  }
  
  .register-success {
    color: #4caf50;
    text-align: center;
  }
  
  .login-text {
    color: white;
    text-align: center;
    font-size: 0.9rem;
  }
  
  .login-link {
    color: red;
    text-decoration: none;
    font-weight: bold;
  }
  </style>
  