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

export const getUserInfo = async (username) => {
  try {
    const response = await axios.get(`http://localhost:5000/api/auth/users/me?username=${username}`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar dados do usuário:", error);
    throw new Error("Erro ao buscar dados do usuário");
  }
};

export const updateUserInfo = async (updatedData) => {
  try {
    const response = await axios.put("http://localhost:5000/api/auth/users/update", updatedData);
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar dados do usuário:", error);
    throw new Error("Erro ao atualizar dados do usuário");
  }
};

