<template>
  <div class="cliente-dashboard">
    <header class="dashboard-header">
      <h1>Bem-vindo, {{ session.username }} (Cliente)</h1>
      <LogoutButton />
    </header>

    <el-tabs v-model="activeTab" type="border-card" class="tabs" stretch>
      <el-tab-pane name="filmes">
        <template #label>
          <el-icon><VideoCamera /></el-icon>
          <span class="tab-label">Filmes em Cartaz</span>
        </template>
        <!-- <FilmesEmCartaz /> -->
        <p class="placeholder">Em breve você poderá ver os filmes disponíveis aqui.</p>
      </el-tab-pane>

      <el-tab-pane name="sessoes">
        <template #label>
          <el-icon><Clock /></el-icon>
          <span class="tab-label">Sessões Disponíveis</span>
        </template>
        <!-- <SessoesDisponiveis /> -->
        <p class="placeholder">Aqui aparecerão as sessões disponíveis para compra.</p>
      </el-tab-pane>

      <el-tab-pane name="ingressos">
        <template #label>
          <el-icon><Ticket /></el-icon>
          <span class="tab-label">Meus Ingressos</span>
        </template>
        <!-- <HistoricoIngressos /> -->
        <p class="placeholder">Seu histórico de ingressos aparecerá aqui.</p>
      </el-tab-pane>

      <el-tab-pane name="conta">
        <template #label>
          <el-icon><User /></el-icon>
          <span class="tab-label">Minha Conta</span>
        </template>
        <!-- <ContaCliente /> -->
        <p class="placeholder">Aqui você poderá ver e editar suas informações de conta.</p>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSessionStore } from '../store/session';
import LogoutButton from '../components/LogoutButton.vue';
import { VideoCamera, Clock, Ticket, User } from '@element-plus/icons-vue';

const session = useSessionStore();
const activeTab = ref('filmes');
</script>

<style scoped>
.cliente-dashboard {
  padding: 2rem;
  color: #fff;
  background-color: #0e0e0e;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.tabs {
  background-color: #1a1a1a;
  border-radius: 1rem;
  padding: 1rem;
}

:deep(.el-tabs__item) {
  background-color: #000000 !important;
  color: #ccc;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  border-radius: 0.5rem 0.5rem 0 0;
  padding: 0.8rem 1.2rem;
  transition: all 0.2s ease;
}

:deep(.el-tabs__item:hover) {
  color: #fff;
  background-color: #2a2a2a !important;
}

:deep(.el-tabs__item.is-active) {
  color: white;
  background-color: #ff0000 !important;
  box-shadow: 0 0 10px red;
  transition: box-shadow 0.3s ease;
}

:deep(.el-tabs__item.is-active:hover) {
  box-shadow: 0 0 20px red;
}

:deep(.el-tabs__content) {
  padding: 1.5rem;
  border: none;
  border-top: 2px solid #ff0000;
  border-radius: 0 0 1rem 1rem;
}

.placeholder {
  color: #ccc;
  padding: 1rem;
  font-size: 1.1rem;
  background-color: transparent;
}

.tab-label {
  margin-left: 4px;
  color: white;
}

:deep(.el-tab-pane) {
  color: #ffffff;
  font-weight: bold;
}

:deep(.el-tab-pane[style*="display: none"]) {
  color: #ccc;
  font-weight: normal;
}
</style>
