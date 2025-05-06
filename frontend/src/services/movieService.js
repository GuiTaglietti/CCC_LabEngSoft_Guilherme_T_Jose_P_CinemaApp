import axios from "axios";
import { ElMessage } from "element-plus";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api",
});

const showSuccess = (message) => {
  ElMessage({
    message: message,
    type: "success",
    duration: 3000,
  });
};

const showError = (error) => {
  ElMessage({
    message: error.response?.data?.message || "Erro inesperado!",
    type: "error",
    duration: 3000,
  });
};

export const fetchMovies = async () => {
  try {
    const response = await api.get("/movies");
    return response.data;
  } catch (error) {
    showError(error);
    throw error;
  }
};

export const createMovie = async (movieData) => {
  try {
    const response = await api.post("/movies/", movieData);
    showSuccess("Filme cadastrado com sucesso!");
    return response.data;
  } catch (error) {
    showError(error);
    throw error;
  }
};

export const updateMovie = async (id, movieData) => {
  try {
    const response = await api.put(`/movies/${id}`, movieData);
    showSuccess("Filme atualizado com sucesso!");
    return response.data;
  } catch (error) {
    showError(error);
    throw error;
  }
};

export const deleteMovie = async (id) => {
  try {
    await api.delete(`/movies/${id}`);
    showSuccess("Filme removido com sucesso!");
  } catch (error) {
    showError(error);
    throw error;
  }
};

export const uploadBanner = async (file) => {
  const formData = new FormData();
  formData.append("banner", file);

  try {
    const response = await api.post("movies/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    showSuccess("Banner enviado com sucesso!");
    return response.data;
  } catch (error) {
    showError(error);
    throw error;
  }
};
