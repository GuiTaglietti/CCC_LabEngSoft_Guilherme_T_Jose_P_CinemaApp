<!-- src/views/ResetPassword.vue -->
<template>
  <div class="reset-container">
    <el-card class="reset-card">
      <h2 class="reset-title">Redefinir Senha</h2>
      <p class="reset-text mb-4">
        Digite sua nova senha abaixo. O link expira em 15 minutos.
      </p>

      <el-form :model="form" status-icon>
        <el-form-item
          label="Nova Senha"
          :error="errors.newPassword"
          prop="newPassword"
        >
          <el-input
            v-model="form.newPassword"
            type="password"
            placeholder="Digite a nova senha"
            show-password
            class="input-field"
          />
        </el-form-item>

        <el-form-item
          label="Confirmar Nova Senha"
          :error="errors.confirmPassword"
          prop="confirmPassword"
        >
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="Confirme a nova senha"
            show-password
            class="input-field"
          />
        </el-form-item>

        <el-button
          type="danger"
          class="reset-button w-100"
          :loading="loading"
          @click="submit"
        >
          Redefinir Senha
        </el-button>

        <p
          v-if="message"
          :class="{ 'success-msg': success, 'error-msg': !success }"
          class="mt-3"
        >
          {{ message }}
        </p>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { resetPassword } from "../services/auth";

const route = useRoute();
const router = useRouter();

const token = ref("");
const form = ref({
  newPassword: "",
  confirmPassword: "",
});
const errors = ref({
  newPassword: "",
  confirmPassword: "",
});
const loading = ref(false);
const message = ref("");
const success = ref(false);

onMounted(() => {
  token.value = route.query.token || "";
  if (!token.value) {
    message.value = "Link de redefinição inválido ou ausente.";
    success.value = false;
  }
});

const validate = () => {
  let valid = true;
  errors.value.newPassword = "";
  errors.value.confirmPassword = "";

  if (!form.value.newPassword) {
    errors.value.newPassword = "A nova senha é obrigatória.";
    valid = false;
  } else if (form.value.newPassword.length < 6) {
    errors.value.newPassword = "A senha deve ter ao menos 6 caracteres.";
    valid = false;
  }

  if (!form.value.confirmPassword) {
    errors.value.confirmPassword = "Por favor, confirme a senha.";
    valid = false;
  } else if (form.value.confirmPassword !== form.value.newPassword) {
    errors.value.confirmPassword = "As senhas não coincidem.";
    valid = false;
  }

  return valid;
};

const submit = async () => {
  if (!validate()) {
    return;
  }

  loading.value = true;
  message.value = "";

  try {
    await resetPassword(token.value, form.value.newPassword);
    message.value = "Senha alterada com sucesso!";
    success.value = true;
    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (err) {
    message.value = err;
    success.value = false;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.reset-container {
  min-height: 100vh;
  background-color: #0d0d0d;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.reset-card {
  background-color: #1a1a1a;
  border: none;
  box-shadow: 0 0 25px rgba(255, 0, 0, 0.5);
  border-radius: 1rem;
  padding: 2.5rem;
  max-width: 480px;
  width: 100%;
  color: #fff;
}

.reset-title {
  text-align: center;
  font-size: 2rem;
  color: #ff4d4f;
  margin-bottom: 1rem;
}

.reset-text {
  text-align: center;
  color: #ccc;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.input-field :deep(.el-input__wrapper) {
  background-color: #2a2a2a;
  border: 1px solid #444;
  border-radius: 0.5rem;
  color: #fff;
}

.input-field :deep(.el-input__inner) {
  color: #fff;
}

.reset-button {
  background-color: #ff0000;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 10px red;
  width: 100%;
}

.reset-button:hover {
  box-shadow: 0 0 20px red;
}

.mt-3 {
  margin-top: 1rem;
}

.success-msg {
  color: #4caf50;
  text-align: center;
}

.error-msg {
  color: #ff4d4f;
  text-align: center;
}
</style>
