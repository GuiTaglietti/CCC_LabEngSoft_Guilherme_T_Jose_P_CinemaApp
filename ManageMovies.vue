<template>
  <div class="movies-header">
    <h1 class="movies-title-header">Gestão de Filmes</h1>
    <el-button
        type="danger"
        @click="goToManagerDashboard"
        class="back-button-header"
      >
        <i class="bi bi-speedometer2" style="margin-right: 0.5rem"></i>
        Voltar ao Painel do Gerente
      </el-button>
  </div>
  <div class="movies-container">
    <div class="movies-card">
      <!-- Carrossel de Filmes -->
      <el-carousel
        :interval="5000"
        type="card"
        arrow="always"
        class="movie-carousel"
      >
        <el-carousel-item v-for="movie in movies" :key="movie.id">
          <div class="movie-item">
            <div class="movie-image">
              <img
                :src="`http://localhost:5000/${movie.banner_url}`"
                alt="Banner do Filme"
                class="movie-banner"
              />
            </div>
            <div class="movie-info">
              <h3 class="movie-title">{{ movie.title }}</h3>
              <p class="movie-description">{{ movie.description }}</p>
              <div class="movie-details">
                <p>
                  <i class="bi bi-film"></i> <strong>Gênero:</strong>
                  {{ movie.genre }}
                </p>
                <p>
                  <i class="bi bi-clock"></i> <strong>Duração:</strong>
                  {{ movie.duration }} minutos
                </p>
                <p>
                  <i class="bi bi-calendar-date"></i>
                  <strong>Lançamento:</strong> {{ movie.release_date }}
                </p>
              </div>
            </div>
            <div class="movie-actions">
              <el-button
                @click="editMovie(movie.id)"
                icon="el-icon-edit"
                size="small"
                type="primary"
              >
                <i class="bi bi-pencil-fill"></i> Editar
              </el-button>
              <el-button
                @click="confirmDelete(movie.id)"
                icon="el-icon-delete"
                size="small"
                type="danger"
              >
                <i class="bi bi-trash-fill"></i> Excluir
              </el-button>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>

      <!-- Dialog para Editar Filme -->
      <el-dialog v-model="isEditing" title="Editar Filme" @close="resetForm">
        <el-input
          v-model="movieForm.title"
          placeholder="Título"
          class="form-input"
        />
        <el-input
          v-model="movieForm.genre"
          placeholder="Gênero"
          class="form-input"
        />
        <el-input
          v-model="movieForm.duration"
          placeholder="Duração (min)"
          type="number"
          class="form-input"
        />
        <el-input
          v-model="movieForm.description"
          type="textarea"
          placeholder="Descrição"
          class="form-input"
        />
        <el-date-picker
          v-model="movieForm.release_date"
          type="date"
          placeholder="Data de Lançamento"
          class="form-input"
        />
        <el-upload
          :action="uploadBannerUrl"
          :on-success="handleBannerUpload"
          :show-file-list="false"
          class="upload-banner"
        >
          <el-button icon="el-icon-upload">Carregar Banner</el-button>
        </el-upload>
        <template #footer>
          <el-button @click="resetForm">Cancelar</el-button>
          <el-button type="primary" @click="saveMovie"
            >Atualizar Filme</el-button
          >
        </template>
      </el-dialog>

      <!-- Dialog para Confirmação de Exclusão -->
      <el-dialog
        v-model="isDeleting"
        title="Confirmar Exclusão"
        @close="resetForm"
        :before-close="closeDeleteDialog"
      >
        <span>Tem certeza que deseja excluir este filme?</span>
        <template #footer>
          <el-button @click="resetForm">Cancelar</el-button>
          <el-button type="danger" @click="deleteMovieConfirmed"
            >Confirmar</el-button
          >
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import {
  fetchMovies,
  updateMovie,
  deleteMovie,
} from "../services/movieService";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      movies: [],
      movieForm: {
        title: "",
        genre: "",
        duration: "",
        description: "",
        release_date: "",
        banner_url: "",
      },
      isEditing: false,
      isDeleting: false,
      currentMovieId: null,
      uploadBannerUrl: "/api/movies/upload",
    };
  },
  methods: {
    async fetchAllMovies() {
      try {
        this.movies = await fetchMovies();
      } catch (error) {
        console.error("Erro ao carregar filmes", error);
      }
    },
    async saveMovie() {
      try {
        if (this.isEditing) {
          await updateMovie(this.currentMovieId, this.movieForm);
          ElMessage.success("Filme atualizado com sucesso!");
        }
        this.fetchAllMovies();
        this.resetForm();
      } catch (error) {
        ElMessage.error("Erro ao atualizar filme");
      }
    },
    editMovie(id) {
      const movie = this.movies.find((movie) => movie.id === id);
      this.movieForm = { ...movie };
      this.isEditing = true;
      this.currentMovieId = id;
    },
    confirmDelete(id) {
      this.currentMovieId = id;
      this.isDeleting = true;
    },
    async deleteMovieConfirmed() {
      try {
        await deleteMovie(this.currentMovieId);
        ElMessage.success("Filme removido com sucesso!");
        this.fetchAllMovies();
        this.resetForm();
      } catch (error) {
        ElMessage.error("Erro ao remover filme");
      }
    },
    handleBannerUpload(response) {
      this.movieForm.banner_url = response.banner_url;
    },
    resetForm() {
      this.movieForm = {
        title: "",
        genre: "",
        duration: "",
        description: "",
        release_date: "",
        banner_url: "",
      };
      this.isEditing = false;
      this.isDeleting = false;
      this.currentMovieId = null;
    },
    closeDeleteDialog() {
      this.isDeleting = false;
    },
    goToManagerDashboard() {
      this.$router.push("/gerente");
    },
  },
  mounted() {
    this.fetchAllMovies();
  },
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.movies-container {
  min-height: 100vh;
  background-color: #121212;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  padding: 0;
}

.movies-card {
  background-color: #1e1e1e;
  color: #f5f5f5;
  border-radius: 0.5rem;
  padding: 2rem;
  max-width: 900px;
  width: 100%;
  box-shadow: 0 0 12px rgba(255, 0, 0, 0.2);
}

.movie-item {
  background-color: #2a2a2a;
  margin-bottom: 1.5rem;
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0 0 5px rgba(255, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.movie-image {
  margin-bottom: 1rem;
  text-align: center;
  max-height: 250px;
  overflow: hidden;
}

.movie-banner {
  width: 100%;
  border-radius: 1rem;
  object-fit: cover;
  height: 100%;
}

.movie-info {
  text-align: left;
  flex-grow: 1;
}

.movie-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ff4d4f;
  margin-bottom: 0.5rem;
}

.movie-description {
  color: #f5f5f5;
  margin-bottom: 1rem;
}

.movie-details {
  font-size: 0.9rem;
  color: #ccc;
}

.movie-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.movie-actions el-button {
  width: 48%;
}

.upload-banner .el-button {
  background-color: #ff4d4f;
  border: none;
  color: white;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: background-color 0.3s ease;
}

.upload-banner .el-button:hover {
  background-color: #cc0000;
}

.el-dialog .el-button--primary {
  background-color: #ff4d4f;
  color: white;
}

.el-dialog .el-button--danger {
  background-color: #cc0000;
  color: white;
}

.el-carousel {
  margin-bottom: 2rem;
}

.el-carousel .el-carousel-item {
  border-radius: 1rem;
  background-color: #2a2a2a;
  color: #fff;
}

.form-input {
  margin-bottom: 1rem;
}

.movies-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background-color: #1e1e1e;
  color: #fff;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
  border-radius: 0;
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
</style>
