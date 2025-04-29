<template>
  <div class="error-container">
    <el-card class="error-card">
      <h2 class="error-title">404 - Página não encontrada</h2>
      <p class="error-message">A pagina acessada não existe.</p>
      <el-button type="danger" class="go-home-button w-100" @click="goHome">
        <i class="bi bi-house-door-fill me-2"></i> Voltar para o login
      </el-button>
    </el-card>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();

    const goHome = () => {
      router.push("/login");
    };

    return { goHome };
  },
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.error-container {
  min-height: 100vh;
  background-color: #0d0d0d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.error-card {
  background-color: #1a1a1a;
  border: none;
  box-shadow: 0 0 25px red;
  border-radius: 1rem;
  padding: 2.5rem;
  max-width: 420px;
  width: 100%;
  text-align: center;
}

.error-title {
  font-size: 2rem;
  color: #fff;
  margin-bottom: 1.5rem;
}

.error-message {
  font-size: 1.2rem;
  color: #fff;
  margin-bottom: 2rem;
}

.go-home-button {
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

.go-home-button:hover {
  box-shadow: 0 0 20px red;
}
</style>
