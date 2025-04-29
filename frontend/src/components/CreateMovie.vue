<template>
  <div class="create-movie-page">
    <div class="form-card">
      <h2 class="mb-4 text-center">Cadastrar Novo Filme</h2>

      <el-form :model="movie" ref="formRef" label-position="top" class="form">
        <el-form-item label="Nome do Filme" prop="title" required>
          <el-input
            v-model="movie.title"
            placeholder="Digite o nome do filme"
          />
        </el-form-item>

        <el-form-item label="Duração (minutos)" prop="duration" required>
          <el-input
            v-model.number="movie.duration"
            type="number"
            placeholder="Ex: 120"
          />
        </el-form-item>

        <el-form-item label="Gênero" prop="genre" required>
          <el-input
            v-model="movie.genre"
            placeholder="Ex: Ação, Drama, Comédia..."
          />
        </el-form-item>

        <el-form-item label="Descrição" prop="description" required>
          <el-input
            v-model="movie.description"
            type="textarea"
            placeholder="Digite uma breve descrição do filme"
          />
        </el-form-item>

        <div class="button-container">
          <el-button
            type="primary"
            @click="submitForm"
            :loading="loading"
            size="large"
          >
            <i class="bi bi-plus-circle me-2"></i> Cadastrar Filme
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { createMovie } from "../services/movieService";
import { useRouter } from "vue-router";

const router = useRouter();

const movie = ref({
  title: "",
  duration: null,
  genre: "",
  description: "",
});

const loading = ref(false);
const formRef = ref(null);

const submitForm = async () => {
  if (
    !movie.value.title ||
    !movie.value.duration ||
    !movie.value.genre ||
    !movie.value.description
  ) {
    ElMessage.error("Por favor, preencha todos os campos.");
    return;
  }

  loading.value = true;
  try {
    await createMovie(movie.value);
    ElMessage.success("Filme cadastrado com sucesso!");
    router.push("/gerente/dashboard");
  } catch (error) {
    console.error(error);
    ElMessage.error("Erro ao cadastrar filme.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.create-movie-page {
  min-height: 100vh;
  background-color: #121212;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.form-card {
  background-color: #1e1e1e;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(255, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
}

h2 {
  color: #ffffff;
}

.form :deep(.el-form-item__label) {
  color: #ffffff;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.el-button {
  background-color: #ff4d4d;
  border: none;
}

.el-button:hover {
  background-color: #ff3333;
}
</style>
