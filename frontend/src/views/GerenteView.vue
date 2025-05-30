<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1 class="dashboard-title">Painel de Controle - Gerente</h1>
      <LogoutButton />
    </div>
    <div class="dashboard-content">
      <div class="dashboard-info">
        <div class="info-card">
          <h4>Data Atual</h4>
          <p>{{ currentDate }}</p>
        </div>
        <div class="info-card">
          <h4>Vendas Realizadas</h4>
          <p>{{ salesCount }} Vendas</p>
        </div>
        <div class="info-card">
          <h4>Filmes em Cartaz</h4>
          <p>{{ moviesOnDisplay }} Filmes</p>
        </div>
        <div class="info-card">
          <h4>Última Requisição de Manutenção</h4>
          <p>{{ currentDate }}</p>
        </div>
      </div>

      <el-carousel trigger="click" arrow="always" class="carousel">
        <el-carousel-item>
          <div class="dashboard-card">
            <i class="bi bi-calendar-plus" style="font-size: 3rem"></i>
            <h3>Criar Sessões</h3>
            <p>Gerencie as sessões de filmes em nosso cinema.</p>
            <el-button type="danger" @click="navigateToCreateSession"
              >Criar Sessão</el-button
            >
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="dashboard-card">
            <i class="bi bi-film" style="font-size: 3rem"></i>
            <h3>Cadastrar Filmes</h3>
            <p>Adicione novos filmes à nossa grade.</p>
            <el-button type="danger" @click="navigateToCreateMovie"
              >Cadastrar Filme</el-button
            >
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="dashboard-card">
            <i class="bi bi-pencil-square" style="font-size: 3rem"></i>
            <h3>Gerenciar Filmes</h3>
            <p>Edite ou exclua filmes existentes.</p>
            <el-button type="danger" @click="navigateToManageMovies"
              >Gerenciar Filmes</el-button
            >
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="dashboard-card">
            <i class="bi bi-bar-chart" style="font-size: 3rem"></i>
            <h3>Relatórios</h3>
            <p>Gere relatórios de desempenho do cinema.</p>
            <el-button type="danger" @click="openDialog"
              >Gerar Relatórios</el-button
            >
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="dashboard-card">
            <i class="bi bi-tools" style="font-size: 3rem"></i>
            <h3>Notificar Manutenção</h3>
            <p>Informe quando um equipamento apresentar problemas.</p>
            <el-button type="danger" @click="navigateToMaintenanceNotification"
              >Notificar Manutenção</el-button
            >
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="dashboard-card">
            <i class="bi bi-eye" style="font-size: 3rem"></i>
            <h3>Visualizar Assentos</h3>
            <p>Veja os assentos vendidos para cada sessão.</p>
            <el-button type="danger" @click="openSessionsDialog">
              Ver Sessões
            </el-button>
          </div>
        </el-carousel-item>
      </el-carousel>

      <el-dialog
        v-model="dialogVisible"
        width="50%"
        :close-on-click-modal="false"
        class="relatorio-dialog"
      >
        <RelatoriosGerente />
        <template #footer>
          <el-button @click="dialogVisible = false">Fechar</el-button>
        </template>
      </el-dialog>

      <el-dialog
        v-model="sessionSeatsDialogVisible"
        title="Mapa de Assentos"
        width="60%"
      >
        <template #default>
          <el-select
            v-model="selectedSessionId"
            placeholder="Selecione uma sessão"
            @change="fetchSeatsForSession"
          >
            <el-option
              v-for="session in sessions"
              :key="session.id"
              :label="`${session.movie_title} - Sala ${
                session.room
              } - ${formatDate(session.start_time)}`"
              :value="session.id"
            />
          </el-select>

          <div v-if="sessionSeats.length" class="seats-wrapper mt-4">
            <div class="seats-grid">
              <el-button
                v-for="seat in sessionSeats"
                :key="seat.id"
                :type="seat.is_occupied ? 'danger' : 'success'"
                :disabled="true"
                class="seat-button"
              >
                {{ seat.seat_number }}
              </el-button>
            </div>
          </div>

          <div v-else class="text-center mt-4 text-light">
            Nenhum assento disponível.
          </div>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import LogoutButton from "../components/LogoutButton.vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "../store/session";
import RelatoriosGerente from "../components/RelatoriosGerente.vue";

const session = useSessionStore();
const router = useRouter();

if (session.role !== "gerente") {
  router.push("/");
}

const currentDate = ref("");
const salesCount = ref(0);
const moviesOnDisplay = ref(0);
const lastMaintenance = ref("");
const sessions = ref([]);
const sessionSeatsDialogVisible = ref(false);
const selectedSessionId = ref(null);
const sessionSeats = ref([]);
const dialogVisible = ref(false);

const updateCurrentDate = () => {
  const date = new Date();
  currentDate.value = date.toLocaleDateString("pt-BR");
};

const openDialog = () => {
  dialogVisible.value = true;
};

const navigateToCreateSession = () => {
  router.push("/gerente/gerenciar-sessoes");
};

const navigateToCreateMovie = () => {
  router.push({ path: "/gerente/cadastrar-filme" });
};

const navigateToManageMovies = () => {
  router.push({ path: "/gerente/gerenciar-filmes" });
};

const navigateToMaintenanceNotification = () => {
  router.push("/gerente/notificar-manutencao");
};

const fetchMoviesCount = async () => {
  try {
    const response = await axios.get("http://localhost:5000/api/movies");
    moviesOnDisplay.value = response.data.length;
  } catch (err) {
    console.error("Erro ao buscar filmes:", err);
  }
};

const fetchSalesCount = async () => {
  try {
    const response = await axios.get("http://localhost:5000/api/tickets/total");
    salesCount.value = response.data.total;
  } catch (err) {
    console.error("Erro ao buscar total de vendas:", err);
  }
};

const fetchSessions = async () => {
  try {
    const response = await axios.get("http://localhost:5000/api/sessions");
    sessions.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar sessões:", err);
  }
};

const openSessionsDialog = async () => {
  await fetchSessions();
  sessionSeatsDialogVisible.value = true;
};

const fetchSeatsForSession = async (sessionId) => {
  try {
    const response = await axios.get(
      `http://localhost:5000/api/tickets/seats/${sessionId}`
    );
    sessionSeats.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar assentos:", err);
  }
};

const formatDate = (str) => {
  const d = new Date(str);
  return d.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(() => {
  updateCurrentDate();
  fetchMoviesCount();
  fetchSalesCount();
});
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.dashboard-container {
  min-height: 100vh;
  background-color: #0d0d0d;
  display: flex;
  flex-direction: column;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  color: white;
  justify-content: center;
  align-items: center;
  padding-top: 4rem;
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
  margin-top: 3rem;
}

.dashboard-info {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-bottom: 2rem;
}

.info-card {
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  text-align: center;
  color: #fff;
  width: 20%;
}

.info-card h4 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.info-card p {
  font-size: 1rem;
  font-weight: bold;
}

.carousel {
  width: 80%;
  max-width: 1200px;
}

.dashboard-card {
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  text-align: center;
  color: #fff;
}

.dashboard-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.dashboard-card p {
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.el-button {
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

.el-button:hover {
  box-shadow: 0 0 20px red;
}

:deep(.el-dialog) {
  background-color: #0e0e0e !important;
  border: 2px solid #ff0000;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
  color: white;
}

.seats-wrapper {
  display: flex;
  justify-content: center;
}

.seats-grid {
  display: grid;
  grid-template-columns: repeat(10, 60px);
  gap: 0.5rem;
  justify-content: center;
}

.seat-button {
  font-weight: bold;
  width: 60px;
  height: 40px;
  text-align: center;
  padding: 0;
}
</style>
