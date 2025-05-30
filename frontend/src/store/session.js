import { defineStore } from "pinia";
import { ref } from "vue";

export const useSessionStore = defineStore("session", () => {
  const token = ref(null);
  const role = ref(null);
  const username = ref(null);
  const userId = ref(null);

  const setSession = (accessToken) => {
    token.value = accessToken;
    const payload = JSON.parse(atob(accessToken.split(".")[1]));

    role.value = payload.sub?.role || payload.role;
    username.value = payload.sub?.username || payload.username;
    userId.value = payload.sub?.user_id || payload.user_id;

    localStorage.setItem("token", accessToken);
    localStorage.setItem("role", role.value);
    localStorage.setItem("username", username.value);
    localStorage.setItem("user_id", userId.value);
  };

  const clearSession = () => {
    token.value = null;
    role.value = null;
    username.value = null;
    userId.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("username");
    localStorage.removeItem("user_id");
  };

  const loadSessionFromStorage = () => {
    const savedToken = localStorage.getItem("token");
    const savedRole = localStorage.getItem("role");
    const savedUsername = localStorage.getItem("username");
    const savedUserId = localStorage.getItem("user_id");

    if (savedToken) {
      token.value = savedToken;
      role.value = savedRole;
      username.value = savedUsername;
      userId.value = savedUserId;
    }
  };

  return {
    token,
    role,
    username,
    userId,
    setSession,
    clearSession,
    loadSessionFromStorage,
  };
});
