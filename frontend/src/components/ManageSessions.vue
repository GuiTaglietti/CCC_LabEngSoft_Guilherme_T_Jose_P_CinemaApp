<template>
  <div class="page-container">
    <div class="movies-header">
      <h1 class="movies-title-header">Gestão de Sessões</h1>
      <el-button
        type="danger"
        @click="goToManagerDashboard"
        class="back-button-header"
      >
        <i class="bi bi-speedometer2" style="margin-right: 0.5rem"></i>
        Voltar ao Painel do Gerente
      </el-button>
    </div>

    <div class="session-container">
      <el-card class="session-card">
        <div class="header-actions mb-2">
          <el-button
            type="danger"
            size="small"
            class="btn-action"
            @click="openSessionDialog"
          >
            <i class="bi bi-plus-circle-fill me-2"></i> Nova Sessão
          </el-button>
        </div>

        <el-table :data="sessions" class="custom-table">
          <el-table-column prop="movie_title" label="Filme"></el-table-column>
          <el-table-column prop="room" label="Sala"></el-table-column>
          <el-table-column label="Início">
            <template #default="scope">
              {{ formatDate(scope.row.start_time) }}
            </template>
          </el-table-column>

          <el-table-column label="Término">
            <template #default="scope">
              {{ formatDate(scope.row.end_time) }}
            </template>
          </el-table-column>

          <el-table-column label="Ações">
            <template #default="scope">
              <div
                class="d-flex flex-column justify-content-center text-center"
              >
                <el-button
                  size="small"
                  type="primary"
                  class="btn-action"
                  @click="editSession(scope.row)"
                >
                  <i class="bi bi-pencil-fill me-2"></i> Editar
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  class="btn-action"
                  @click="confirmDelete(scope.row.id)"
                >
                  <i class="bi bi-trash-fill me-2"></i> Excluir
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <el-dialog
      v-model="isEditing"
      :title="sessionForm.id ? 'Editar Sessão' : 'Nova Sessão'"
      class="custom-dialog"
    >
      <el-form label-position="top">
        <el-form-item label="Filme">
          <el-select
            v-model="sessionForm.movie_id"
            placeholder="Selecione o Filme"
            class="custom-input"
          >
            <el-option
              v-for="movie in movies"
              :key="movie.id"
              :label="movie.title"
              :value="movie.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Sala">
          <el-input
            v-model="sessionForm.room"
            placeholder="Sala"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Início">
          <el-date-picker
            v-model="sessionForm.start_time"
            type="datetime"
            placeholder="Início"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Término">
          <el-date-picker
            v-model="sessionForm.end_time"
            type="datetime"
            placeholder="Término"
            class="custom-input"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="resetForm">Cancelar</el-button>
        <el-button type="danger" class="btn-action" @click="saveSession">
          <i class="bi bi-save-fill me-2"></i> Salvar
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="isDeleting"
      title="Confirmar Exclusão"
      class="custom-dialog"
    >
      <span>Tem certeza que deseja excluir esta sessão?</span>
      <template #footer>
        <el-button @click="resetForm">Cancelar</el-button>
        <el-button
          type="danger"
          class="btn-action"
          @click="deleteSessionConfirmed"
        >
          <i class="bi bi-check-circle-fill me-2"></i> Confirmar
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { fetchMovies } from "../services/movieService";
import {
  fetchSessions,
  createSession,
  updateSession,
  deleteSession,
} from "../services/sessionService";

export default {
  data() {
    return {
      movies: [],
      sessions: [],
      isEditing: false,
      isDeleting: false,
      currentSessionId: null,
      sessionForm: {
        id: null,
        movie_id: "",
        room: "",
        start_time: "",
        end_time: "",
      },
    };
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      this.movies = await fetchMovies();
      this.sessions = await fetchSessions();
    },
    openSessionDialog() {
      this.resetForm();
      this.isEditing = true;
    },
    editSession(session) {
      this.sessionForm = { ...session };
      this.isEditing = true;
      this.currentSessionId = session.id;
    },
    async saveSession() {
      try {
        const payload = {
          movie_id: this.sessionForm.movie_id,
          room: this.sessionForm.room,
          start_time: this.sessionForm.start_time,
          end_time: this.sessionForm.end_time,
        };

        if (this.currentSessionId) {
          await updateSession(this.currentSessionId, payload);
        } else {
          await createSession(payload);
        }

        await this.loadData();
        this.resetForm();
      } catch (error) {
        // Erro tratado no service
      }
    },
    confirmDelete(id) {
      this.currentSessionId = id;
      this.isDeleting = true;
    },
    async deleteSessionConfirmed() {
      try {
        await deleteSession(this.currentSessionId);
        await this.loadData();
        this.resetForm();
      } catch (error) {
        // Erro tratado no service
      }
    },
    resetForm() {
      this.isEditing = false;
      this.isDeleting = false;
      this.currentSessionId = null;
      this.sessionForm = {
        id: null,
        movie_id: "",
        room: "",
        start_time: "",
        end_time: "",
      };
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      const options = {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return date.toLocaleString("pt-BR", options).replace(",", " -");
    },
    goToManagerDashboard() {
      this.$router.push("/gerente");
    },
  },
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.page-container {
  background-color: #0d0d0d;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  color: white;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.movies-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background-color: #1e1e1e;
  color: #fff;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
  position: sticky;
  top: 0;
  z-index: 10;
}

.movies-title-header {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ff4d4f;
}

.back-button-header {
  background-color: #ff4d4f;
  border: none;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.back-button-header:hover {
  background-color: #cc0000;
}

.session-container {
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.session-card {
  background-color: #1a1a1a;
  border-radius: 1rem;
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  box-shadow: 0 0 25px red;
}

.custom-table {
  background-color: transparent;
  color: rgb(0, 0, 0);
}

.el-table th {
  background-color: #ff0000;
  color: white;
}

.el-table td {
  background-color: #0d0d0d;
  color: white;
}

.btn-action {
  background-color: #ff0000;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  margin: 0.25rem;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 10px red;
}

.btn-action:hover {
  box-shadow: 0 0 20px red;
}

.custom-dialog {
  background-color: #1a1a1a;
  color: white;
}
</style>
