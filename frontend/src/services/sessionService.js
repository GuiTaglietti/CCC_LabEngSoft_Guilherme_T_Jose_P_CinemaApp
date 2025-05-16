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
    const data = error.response?.data;
    ElMessage({
      message: data?.error || data?.message || "Erro inesperado!",
      type: "error",
      duration: 3000,
    });
};
  

export const fetchSessions = async () => {
  try {
    const response = await api.get("/sessions/");
    return response.data;
  } catch (error) {
    showError(error);
    throw error;
  }
};

export const createSession = async (sessionData) => {
  try {
    const response = await api.post("/sessions/", sessionData);
    showSuccess("Sessão criada com sucesso!");
    return response.data;
  } catch (error) {
    showError(error);
    throw error;
  }
};

export const updateSession = async (id, sessionData) => {
  try {
    const response = await api.put(`/sessions/${id}`, sessionData);
    showSuccess("Sessão atualizada com sucesso!");
    return response.data;
  } catch (error) {
    showError(error);
    throw error;
  }
};

export const deleteSession = async (id) => {
  try {
    await api.delete(`/sessions/${id}`);
    showSuccess("Sessão excluída com sucesso!");
  } catch (error) {
    showError(error);
    throw error;
  }
};