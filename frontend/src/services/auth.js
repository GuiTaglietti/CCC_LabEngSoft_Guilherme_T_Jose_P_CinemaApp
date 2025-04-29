import axios from "axios";

export const login = async (username, password) => {
  try {
    const response = await axios.post("http://localhost:5000/api/auth/login", {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    console.error("Login falhou:", error);
    throw new Error("Login falhou");
  }
};

export const register = async (userData) => {
  try {
    const response = await axios.post("http://localhost:5000/api/auth/register", userData);
    return response.data;
  } catch (error) {
    console.error("Registro falhou:", error);
    throw error.response?.data?.msg || new Error("Registro falhou");
  }
};

export const recoverPassword = async (email) => {
  try {
    const response = await axios.post("http://localhost:5000/api/auth/recoverpassword", { email });
    return response.data;
  } catch (error) {
    console.error("Erro ao recuperar senha:", error);
    throw new Error("Erro ao recuperar senha");
  }
};