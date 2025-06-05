<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1 class="dashboard-title">Solicitar Manutenção</h1>
      <el-button
        type="danger"
        @click="goToManagerDashboard"
        class="back-button-header"
      >
        <i class="bi bi-speedometer2" style="margin-right: 0.5rem"></i>
        Voltar ao Painel do Gerente
      </el-button>
    </div>
    <div class="dashboard-content">
      <div class="dashboard-card">
        <h3 class="mb-2">Descreva o Problema</h3>
        <p class="mb-2">
          Informe qual equipamento está com defeito e o que está acontecendo.
        </p>
        <el-input
          type="textarea"
          v-model="message"
          placeholder="Ex: O projetor da sala 3 está desligando sozinho."
          rows="6"
          class="maintenance-textarea"
        />
        <el-button
          type="danger"
          class="btn-danger mt-4"
          @click="sendMessage"
          :disabled="loading"
        >
          <span v-if="loading">Enviando...</span>
          <span v-else>Enviar Notificação</span>
        </el-button>
      </div>
    </div>

    <!-- Caixa de diálogo de confirmação -->
    <el-dialog
      v-model="dialogVisible"
      title="Notificação Enviada"
      :close-on-click-modal="false"
      :show-close="false"
      class="success-dialog"
    >
      <span>
        A solicitação de manutenção foi enviada com sucesso! Verifique seu e-mail
        para mais detalhes.
      </span>
      <template #footer>
        <el-button type="primary" class="dialog-button" @click="closeDialog">
          OK
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "../store/session";
import { sendMaintenanceMessage } from "../services/maintenanceService";
import { ElMessage } from "element-plus";

const session = useSessionStore();
const router = useRouter();

if (session.role !== "gerente") {
  router.push("/");
}

const message = ref("");
const loading = ref(false);
const dialogVisible = ref(false);

const sendMessage = async () => {
  if (!message.value.trim()) {
    ElMessage.warning("Por favor, descreva o problema antes de enviar.");
    return;
  }

  loading.value = true;
  try {
    await sendMaintenanceMessage(session.username, message.value);
    dialogVisible.value = true;
    message.value = "";
  } catch (error) {
    console.error("Erro ao enviar mensagem de manutenção:", error);
    ElMessage.error("Erro ao enviar mensagem. Tente novamente.");
  } finally {
    loading.value = false;
  }
};

const closeDialog = () => {
  dialogVisible.value = false;
  goToManagerDashboard();
};

const goToManagerDashboard = () => {
  router.push("/gerente");
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {
  overflow-x: hidden;
}

.dashboard-container {
  min-height: 100vh;
  width: 100vw;
  background-color: #0d0d0d;
  display: flex;
  flex-direction: column;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  color: white;
  justify-content: center;
  align-items: center;
  padding-top: 4rem;
  overflow-x: hidden;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1a1a1a;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
}

.dashboard-title {
  font-size: 2.5rem;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 2rem;
  margin-top: 5rem;
  max-width: 100%;
  overflow-x: hidden;
}

.dashboard-card {
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  text-align: center;
  color: #fff;
  width: 100%;
  max-width: 600px;
  overflow-wrap: break-word;
  word-break: break-word;
}

.maintenance-textarea :deep(.el-textarea__inner) {
  background-color: #2a2a2a;
  color: white;
  border: 1px solid #444;
  font-size: 1rem;
  border-radius: 0.5rem;
}

.maintenance-textarea :deep(.el-textarea__inner::placeholder) {
  color: #bbb;
}

.el-button {
  background-color: #ff0000;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 10px red;
  cursor: pointer;
}

.el-button:hover {
  box-shadow: 0 0 20px red;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.mt-4 {
  margin-top: 1rem;
}

/* Diálogo de sucesso */
.success-dialog .el-dialog__header {
  background-color: #1a1a1a;
  color: #fff;
  border-bottom: 2px solid #ff0000;
}

.success-dialog .el-dialog__body {
  background-color: #1a1a1a;
  color: #fff;
  font-size: 1rem;
  padding: 20px;
}

.success-dialog .dialog-button {
  background-color: #ff0000;
  color: white;
  font-weight: bold;
  border-radius: 0.5rem;
  padding: 0.75rem 1.5rem;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 10px red;
}

.success-dialog .dialog-button:hover {
  box-shadow: 0 0 20px red;
}

.back-button-header {
  background-color: transparent;
  color: #ff0000;
  border: 1px solid #ff0000;
  font-weight: bold;
}

.back-button-header:hover {
  background-color: #ff0000;
  color: #fff;
}
</style>
