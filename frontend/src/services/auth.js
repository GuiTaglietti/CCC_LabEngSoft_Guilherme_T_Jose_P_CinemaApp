import axios from "axios";

export const login = async (username, password) => {
  try {
    const response = await axios.post("http://localhost:5000/api/auth/login", {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    console.error("Login failed:", error);
    throw new Error("Login failed");
  }
};
