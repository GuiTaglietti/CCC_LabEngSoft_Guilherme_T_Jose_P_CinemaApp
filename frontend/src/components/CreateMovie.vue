<template>
  <div class="movies-header">
    <h1 class="movies-title-header">Cadastro de Filmes</h1>
    <el-button
      type="danger"
      icon="el-icon-arrow-left"
      @click="goToManagerDashboard"
      class="back-button-header"
    >
      Voltar ao Painel do Gerente
    </el-button>
  </div>
  <div class="movie-container">
    <el-card class="movie-card">
      <h2 class="movie-title">Cadastrar Novo Filme</h2>

      <el-form :model="movie" label-width="140px" @submit.prevent="submitForm">
        <el-form-item label="Título do Filme" prop="title">
          <el-input
            v-model="movie.title"
            placeholder="Digite o título"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Duração (min)" prop="duration">
          <el-input-number
            v-model="movie.duration"
            :min="1"
            class="custom-input-number"
          />
        </el-form-item>

        <el-form-item label="Gênero" prop="genre">
          <el-input
            v-model="movie.genre"
            placeholder="Digite o gênero"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Descrição" prop="description">
          <el-input
            type="textarea"
            v-model="movie.description"
            placeholder="Digite a descrição"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Lançamento" prop="release_date">
          <el-date-picker
            v-model="movie.release_date"
            type="date"
            placeholder="Escolha a data"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Banner" prop="banner">
          <el-upload
            class="upload-banner"
            drag
            action=""
            :http-request="handleBannerUpload"
            :show-file-list="false"
          >
            <i class="bi bi-cloud-arrow-up fs-1 upload-icon"></i>
            <div class="el-upload__text upload-text">
              Clique ou arraste o banner aqui
            </div>
          </el-upload>
        </el-form-item>

        <template v-if="movie.banner_url">
          <div class="text-center mb-3">
            <img
              :src="`http://localhost:5000/${movie.banner_url}`"
              alt="Banner do Filme"
              class="banner-preview"
            />
          </div>
        </template>

        <el-form-item>
          <el-button type="danger" class="submit-button" @click="submitForm">
            <i class="bi bi-plus-circle me-2"></i> Cadastrar
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { createMovie, uploadBanner } from "../services/movieService";
import { useRouter } from "vue-router";

const router = useRouter();

const movie = ref({
  title: "",
  duration: null,
  genre: "",
  description: "",
  release_date: "",
  banner_url: "",
});

const handleBannerUpload = async ({ file }) => {
  try {
    const { banner_url } = await uploadBanner(file);
    movie.value.banner_url = banner_url;
  } catch (error) {
    // O erro já é tratado dentro do service
  }
};

const submitForm = async () => {
  try {
    await createMovie(movie.value);
    resetForm();
  } catch (error) {
    // O erro já é tratado dentro do service
  }
};

const resetForm = () => {
  movie.value = {
    title: "",
    duration: null,
    genre: "",
    description: "",
    release_date: "",
    banner_url: "",
  };
};

const goToManagerDashboard = () => {
  router.push("/gerente");
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.movie-container {
  min-height: 100vh;
  background-color: #0d0d0d;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 1rem;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.movie-card {
  background-color: #1a1a1a;
  border: none;
  box-shadow: 0 0 25px red;
  border-radius: 1rem;
  padding: 2.5rem;
  width: 100%;
  max-width: 720px;
}

.movie-title {
  color: #fff;
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
}

.custom-input :deep(.el-input__wrapper),
.custom-input-number :deep(.el-input-number__decrease),
.custom-input-number :deep(.el-input-number__increase),
.custom-input-number :deep(.el-input__wrapper),
.custom-input :deep(.el-input__inner),
.custom-input-number :deep(.el-input__inner),
:deep(.el-date-editor),
:deep(.el-date-editor .el-input__wrapper),
:deep(.el-date-editor .el-input__inner),
:deep(.el-textarea .el-textarea__inner) {
  background-color: #111 !important;
  color: white !important;
  border-radius: 0.5rem;
}

:deep(.el-input__prefix),
:deep(.el-input__suffix),
:deep(.el-icon),
:deep(.el-input__prefix-inner) {
  color: white !important;
}

:deep(.el-input__inner)::placeholder,
:deep(.el-textarea__inner)::placeholder {
  color: #ccc !important;
}

.upload-banner {
  border: 2px dashed #ff0000;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  transition: border-color 0.3s, background-color 0.3s;
  background-color: #1a1a1a;
  color: white;
}

.upload-banner:hover {
  border-color: #ff4d4f;
  background-color: #222;
}

.upload-icon {
  font-size: 3rem;
  color: #ff4d4f;
  margin-bottom: 0.5rem;
}

.upload-text {
  color: #ddd;
  font-size: 1rem;
}

.banner-preview {
  max-width: 100%;
  border-radius: 0.5rem;
  box-shadow: 0 0 10px red;
}

.submit-button {
  background-color: #ff0000;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 10px red;
}

.submit-button:hover {
  box-shadow: 0 0 20px red;
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
  border-radius: 0; /* Remove arredondamento nas bordas */
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
