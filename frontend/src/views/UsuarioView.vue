<template>
  <div class="cliente-dashboard">
    <header class="dashboard-header">
      <h1>Bem-vindo, {{ session.username }}</h1>
      <LogoutButton />
    </header>

    <el-tabs v-model="activeTab" type="border-card" class="tabs" stretch>
      <el-tab-pane name="filmes">
        <template #label>
          <el-icon><VideoCamera /></el-icon>
          <span class="tab-label">Filmes em Cartaz</span>
        </template>

        <!-- Carrossel de filmes -->
        <el-carousel
          :interval="6000"
          arrow="always"
          type="card"
          height="480px"
          class="carousel-custom"
        >
          <el-carousel-item v-for="movie in movies" :key="movie.id">
            <div class="carousel-movie">
              <img
                :src="`http://localhost:5000/${movie.banner_url}`"
                class="carousel-banner"
              />
              <div class="carousel-details">
                <h2 class="movie-title">
                  <i class="bi bi-film me-2"></i> {{ movie.title }}
                </h2>
                <p class="movie-description">
                  <i class="bi bi-info-circle me-2"></i> {{ movie.description }}
                </p>
                <div class="movie-meta">
                  <p>
                    <i class="bi bi-tags me-2"></i> <strong>Gênero:</strong>
                    {{ movie.genre }}
                  </p>
                  <p>
                    <i class="bi bi-clock me-2"></i> <strong>Duração:</strong>
                    {{ movie.duration }} min
                  </p>
                  <p>
                    <i class="bi bi-calendar me-2"></i>
                    <strong>Lançamento:</strong>
                    {{ formatDate(movie.release_date) }}
                  </p>
                </div>
                <div class="text-center mt-3">
                  <el-button
                    class="session-button"
                    @click="openSessionDialog(movie.id)"
                  >
                    <i class="bi bi-eye me-2"></i> Visualizar Sessões
                  </el-button>
                </div>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>

        <!-- Dialog de sessões -->
        <el-dialog
          v-model="sessionDialogVisible"
          width="50%"
          class="session-dialog"
          :show-close="false"
        >
          <template #header>
            <div class="dialog-header">
              <h3 class="dialog-title">Sessões Disponíveis</h3>
              <el-button
                type="danger"
                circle
                @click="sessionDialogVisible = false"
              >
                <span class="bi bi-x-lg"></span>
              </el-button>
            </div>
          </template>

          <div class="dialog-body">
            <div v-if="selectedSessions.length">
              <ul class="session-list">
                <li
                  v-for="(session, index) in selectedSessions"
                  :key="session.id"
                  class="session-item"
                >
                  <h4 class="session-title">Sessão #{{ index + 1 }}</h4>
                  <div class="session-content">
                    <p>
                      <i class="bi bi-door-open me-2 text-danger"></i>
                      <strong>Sala:</strong> {{ session.room }}
                    </p>
                    <p>
                      <i class="bi bi-play-circle me-2 text-danger"></i>
                      <strong>Início:</strong>
                      {{ formatDate(session.start_time) }}
                    </p>
                    <p>
                      <i class="bi bi-stop-circle me-2 text-danger"></i>
                      <strong>Término:</strong>
                      {{ formatDate(session.end_time) }}
                    </p>
                  </div>
                </li>
              </ul>
            </div>
            <div v-else>
              <p>Este filme ainda não possui sessões cadastradas.</p>
            </div>
          </div>
        </el-dialog>
      </el-tab-pane>

      <!-- Sessões -->
      <el-tab-pane name="sessoes">
        <template #label>
          <el-icon><Clock /></el-icon>
          <span class="tab-label">Sessões Disponíveis</span>
        </template>
        <div class="session-cards">
          <div
            v-for="session in sessions"
            :key="session.id"
            class="session-card"
          >
            <h3>
              <i class="bi bi-film text-danger me-2"></i>
              {{ getMovieTitle(session.movie_id) }}
            </h3>
            <p>
              <i class="bi bi-door-open text-danger me-2"></i>
              <strong>Sala:</strong> {{ session.room }}
            </p>
            <p>
              <i class="bi bi-play-circle text-danger me-2"></i>
              <strong>Início:</strong> {{ formatDate(session.start_time) }}
            </p>
            <p>
              <i class="bi bi-stop-circle text-danger me-2"></i>
              <strong>Término:</strong> {{ formatDate(session.end_time) }}
            </p>
            <el-button
              type="danger"
              class="buy-button"
              @click="openPurchaseDialog(session)"
            >
              <i class="bi bi-cart-plus me-2"></i> Comprar Ingresso
            </el-button>
          </div>
        </div>

        <el-dialog
          v-model="purchaseDialogVisible"
          title="Comprar Ingresso"
          width="50%"
        >
          <div>
            <p>
              <strong>Filme:</strong>
              {{ getMovieTitle(selectedSession?.movie_id) }}
            </p>
            <p><strong>Sala:</strong> {{ selectedSession?.room }}</p>
            <p>
              <strong>Início:</strong>
              {{ formatDate(selectedSession?.start_time) }}
            </p>
            <p>
              <strong>Fim:</strong> {{ formatDate(selectedSession?.end_time) }}
            </p>
            <p><strong>Escolha o assento:</strong></p>

            <div class="seats-row">
              <el-button
                v-for="seat in seats.filter((seat) =>
                  seat.seat_number.startsWith('A')
                )"
                :key="seat.id"
                :type="
                  seat.is_occupied
                    ? 'danger'
                    : selectedSeat?.id === seat.id
                    ? 'primary'
                    : 'success'
                "
                :disabled="seat.is_occupied"
                @click="selectedSeat = seat"
                class="seat-button"
              >
                {{ seat.seat_number }}
              </el-button>
            </div>

            <div class="seats-row">
              <el-button
                v-for="seat in seats.filter((seat) =>
                  seat.seat_number.startsWith('B')
                )"
                :key="seat.id"
                :type="
                  seat.is_occupied
                    ? 'danger'
                    : selectedSeat?.id === seat.id
                    ? 'primary'
                    : 'success'
                "
                :disabled="seat.is_occupied"
                @click="selectedSeat = seat"
                class="seat-button"
              >
                {{ seat.seat_number }}
              </el-button>
            </div>

            <el-select
              v-model="paymentMethod"
              placeholder="Método de pagamento"
            >
              <el-option label="PIX" value="pix"></el-option>
              <el-option
                label="Cartão de Crédito"
                value="credit_card"
              ></el-option>
            </el-select>
          </div>
          <template #footer>
            <el-button @click="purchaseDialogVisible = false"
              >Cancelar</el-button
            >
            <el-button type="primary" @click="confirmPurchase"
              >Confirmar Compra</el-button
            >
          </template>
        </el-dialog>
      </el-tab-pane>

      <!-- Ingressos -->
      <el-tab-pane name="ingressos">
        <template #label>
          <el-icon><Ticket /></el-icon>
          <span class="tab-label">Meus Ingressos</span>
        </template>
        <div v-if="userTickets.length">
          <el-card
            v-for="ticket in userTickets"
            :key="ticket.id"
            class="ticket-card"
            @click="openQrDialog(ticket)"
            style="cursor: pointer"
          >
            <p>
              <i class="bi bi-film"></i><strong>Filme:</strong>
              {{ ticket.title }}
            </p>
            <p>
              <i class="bi bi-grid-3x3-gap"></i><strong>Assento:</strong>
              {{ ticket.seat_number }}
            </p>
            <p>
              <i class="bi bi-play-circle"></i><strong>Início:</strong>
              {{ formatDate(ticket.start_time) }}
            </p>
            <p>
              <i class="bi bi-stop-circle"></i><strong>Fim:</strong>
              {{ formatDate(ticket.end_time) }}
            </p>
            <p>
              <i class="bi bi-credit-card"></i><strong> Status:</strong>
              {{ translatePaymentStatus(ticket.payment_status) }}
            </p>
          </el-card>
        </div>
        <div v-else>
          <p class="placeholder">Nenhum ingresso comprado ainda.</p>
        </div>

        <el-dialog
          v-model="qrDialogVisible"
          title="QR Code do Ingresso"
          width="300px"
          class="qr-dialog"
          :show-close="false"
        >
          <div class="qr-content">
            <qrcode-vue
              :value="`Ingresso ID: ${selectedTicket?.id}`"
              :size="200"
              level="H"
              background="#0e0e0e"
              foreground="#ff0000"
            />
            <p class="qr-text">Apresente este QR Code na entrada</p>
          </div>

          <template #footer>
            <el-button @click="qrDialogVisible = false">Fechar</el-button>
          </template>
        </el-dialog>
      </el-tab-pane>

      <!-- Conta -->
      <el-tab-pane name="conta">
        <template #label>
          <el-icon><User /></el-icon>
          <span class="tab-label">Minha Conta</span>
        </template>
        <div class="account-info">
          <el-form label-position="top" :model="userInfo">
            <el-form-item label="Nome de Usuário">
              <el-input v-model="userInfo.username" disabled />
            </el-form-item>
            <el-form-item label="Nome Completo">
              <el-input v-model="userInfo.full_name" />
            </el-form-item>
            <el-form-item label="Email">
              <el-input v-model="userInfo.email" />
            </el-form-item>
            <el-form-item>
              <el-button class="button-atualizar" @click="updateUserInfo">
                <i class="bi bi-save me-2"></i> Atualizar Dados
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useSessionStore } from "../store/session";
import LogoutButton from "../components/LogoutButton.vue";
import {
  getUserInfo,
  updateUserInfo as updateUserInfoAPI,
} from "../services/auth";
import axios from "axios";
import { ElMessage } from "element-plus";
import QrcodeVue from "qrcode.vue";

const session = useSessionStore();
const activeTab = ref("filmes");
const movies = ref([]);
const sessions = ref([]);
const selectedSessions = ref([]);
const sessionDialogVisible = ref(false);
const purchaseDialogVisible = ref(false);
const selectedSession = ref(null);
const seats = ref([]);
const selectedSeat = ref(null);
const paymentMethod = ref("pix");
const userTickets = ref([]);
const userInfo = ref({ username: session.username, full_name: "", email: "" });
const qrDialogVisible = ref(false);
const selectedTicket = ref(null);

const openQrDialog = (ticket) => {
  selectedTicket.value = ticket;
  qrDialogVisible.value = true;
};

const statusLabel = (status) => {
  const map = {
    paid: "Pago",
    pending: "Pendente",
    canceled: "Cancelado",
  };
  return map[status] || status;
};

const fetchMovies = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/movies");
    movies.value = res.data;
  } catch (err) {
    ElMessage.error("Erro ao buscar filmes:", err);
  }
};

const fetchSessions = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/sessions");
    sessions.value = res.data;
  } catch (err) {
    ElMessage.error("Erro ao buscar sessões:", err);
  }
};

const openSessionDialog = async (movieId) => {
  try {
    const res = await axios.get("http://localhost:5000/api/sessions");
    selectedSessions.value = res.data.filter((s) => s.movie_id === movieId);
    sessionDialogVisible.value = true;
  } catch (err) {
    ElMessage.error("Erro ao buscar sessões:", err);
  }
};

const getMovieTitle = (id) => {
  const movie = movies.value.find((m) => m.id === id);
  return movie ? movie.title : "Título Desconhecido";
};

const updateUserInfo = async () => {
  try {
    await updateUserInfoAPI(userInfo.value);
    ElMessage.success("Dados atualizados com sucesso!");
  } catch (err) {
    ElMessage.success("Erro ao atualizar dados.");
  }
};

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const openPurchaseDialog = async (session) => {
  selectedSession.value = session;
  selectedSeat.value = null;
  paymentMethod.value = "pix";
  purchaseDialogVisible.value = true;

  try {
    const res = await axios.get(
      `http://localhost:5000/api/tickets/seats/${session.id}`
    );
    seats.value = res.data;
  } catch (err) {
    ElMessage.error("Erro ao carregar assentos");
  }
};

const confirmPurchase = async () => {
  if (!selectedSeat.value) {
    ElMessage.error("Selecione um assento");
    return;
  }
  try {
    const payload = {
      user_id: session.userId,
      session_id: selectedSession.value.id,
      seat_id: selectedSeat.value.id,
      payment_method: paymentMethod.value,
      payment_id: "test-payment-id",
    };

    await axios.post("http://localhost:5000/api/tickets/tickets", payload);
    ElMessage.success("Ingresso comprado com sucesso!");

    purchaseDialogVisible.value = false;
    fetchUserTickets();
  } catch (err) {
    ElMessage.error("Erro ao confirmar compra");
  }
};

const fetchUserTickets = async () => {
  try {
    const res = await axios.get(
      `http://localhost:5000/api/tickets/tickets/${session.userId}`
    );
    userTickets.value = res.data;
  } catch (err) {
    ElMessage.error("Erro ao carregar ingressos");
  }
};

const translatePaymentStatus = (status) => {
  const statusMap = {
    paid: "Pago",
    pending: "Pendente",
    cancelled: "Cancelado",
    refunded: "Reembolsado",
    failed: "Falhou",
  };
  return statusMap[status] || status;
};

onMounted(async () => {
  fetchMovies();
  fetchSessions();
  fetchUserTickets();
  try {
    const user = await getUserInfo(session.username);
    userInfo.value = user;
  } catch (e) {
    ElMessage.error("Erro ao carregar dados do usuário", e);
  }
});
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.carousel-custom :deep(.el-carousel__arrow) {
  background-color: rgba(255, 255, 255, 0.3);
  color: #000;
  transition: background-color 0.3s;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.4);
}

.carousel-custom :deep(.el-carousel__arrow:hover) {
  background-color: white;
}

.session-dialog :deep(.el-overlay) {
  background-color: rgba(0, 0, 0, 0.8);
}

.session-dialog :deep(.el-overlay),
.session-dialog :deep(.el-dialog),
.session-dialog :deep(.el-dialog__wrapper) {
  background-color: #0e0e0e !important;
}

.session-dialog :deep(.el-dialog__header),
.session-dialog :deep(.el-dialog__body),
.session-dialog :deep(.el-dialog__footer) {
  background-color: #0e0e0e;
  color: white;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #000;
}

.dialog-body {
  padding-top: 1rem;
}

.session-list {
  list-style: none;
  padding: 0;
}

.session-title {
  color: #ff4d4f;
  font-weight: bold;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.session-content {
  background-color: #000;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
}

.text-danger {
  color: #ff4d4f;
}

.carousel-movie {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #000000;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 0 25px rgba(255, 0, 0, 0.5);
  padding: 1rem;
  height: 100%;
}

.carousel-banner {
  max-height: 240px;
  width: 100%;
  object-fit: cover;
  border-radius: 1rem;
  margin-bottom: 1rem;
}

.carousel-details {
  color: #fff;
  text-align: left;
  width: 100%;
}

.movie-title {
  font-size: 1.5rem;
  color: #ff4d4f;
  margin-bottom: 0.5rem;
}

.movie-description {
  font-size: 1rem;
  color: #ddd;
  margin-bottom: 0.5rem;
}

.movie-meta p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: #ccc;
}

.session-item {
  background-color: #2a2a2a;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  color: white;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
}

.session-button {
  width: 100%;
  max-width: 250px;
  font-weight: bold;
  background: #ff0000;
  color: white;
}

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
  box-shadow: 0 0 20px red;
  transition: box-shadow 0.3s ease;
}

:deep(.el-tabs__item.is-active:hover) {
  box-shadow: 0 0 25px red;
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

.session-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
}

.session-card {
  background: #1a1a1a;
  border-radius: 0.75rem;
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
  padding: 1.25rem;
  flex: 1 1 280px;
  color: white;
}

.buy-button {
  margin-top: 0.75rem;
  background-color: #ff0000;
  color: white;
  border: none;
  font-weight: bold;
  width: 100%;
}

.account-info {
  padding: 2rem;
  max-width: 600px;
  margin: auto;
  background: #1a1a1a;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
  color: white;
}

.button-atualizar {
  background-color: #ff0000;
  color: white;
  font-weight: bold;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  transition: box-shadow 0.3s ease;
}

.seats-row {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.seat-button {
  width: 50px;
  height: 50px;
  padding: 0;
  font-weight: bold;
}

.ticket-card {
  background: #1a1a1a;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
  margin-bottom: 1rem;
  color: white;
}

:deep(.el-dialog) {
  background-color: #0e0e0e !important;
  border: 2px solid #ff0000;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
  color: white;
}

:deep(.el-dialog__header) {
  background-color: #1a1a1a;
  border-bottom: 1px solid #ff0000;
  padding: 1rem;
  font-weight: bold;
  color: #ff4d4f;
  font-size: 1.25rem;
}

:deep(.el-dialog__body) {
  padding: 1.5rem;
  color: #ccc;
}

:deep(.el-dialog__footer) {
  background-color: #1a1a1a;
  border-top: 1px solid #ff0000;
  padding: 1rem;
}

:deep(.el-button) {
  font-weight: bold;
  border-radius: 0.5rem;
}

:deep(.el-button--primary) {
  background-color: #ff0000;
  border-color: #ff0000;
  color: white;
}

:deep(.el-button--danger) {
  background-color: #ff0000;
  border-color: #ff0000;
  color: white;
}

.ticket-card {
  background: linear-gradient(135deg, #1a1a1a, #000);
  border: 1px solid #ff0000;
  border-radius: 1rem;
  padding: 1.25rem;
  margin-bottom: 1rem;
  color: white;
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
  transition: transform 0.2s ease;
}

.ticket-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
}

.ticket-card i {
  color: #ff4d4f;
  margin-right: 0.5rem;
}

.placeholder {
  color: #ccc;
  padding: 1rem;
  font-size: 1.1rem;
  background-color: transparent;
  text-align: center;
  border: 1px dashed #ff0000;
  border-radius: 0.5rem;
}

:deep(.el-select) {
  width: 100%;
  margin-top: 1rem;
}

:deep(.el-select .el-input__inner) {
  background-color: #1a1a1a;
  border: 1px solid #ff0000;
  color: white;
}

.seat-button {
  font-weight: bold;
  transition: transform 0.2s;
}

.seat-button:hover {
  transform: scale(1.05);
}

.qr-dialog :deep(.el-dialog) {
  background-color: #0e0e0e !important;
  border: 2px solid #ff0000;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
  text-align: center;
  padding: 1rem;
}

.qr-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.qr-text {
  margin-top: 1rem;
  color: #fff;
  font-weight: bold;
}
</style>
