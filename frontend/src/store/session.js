import { defineStore } from "pinia";
import { ref } from "vue";

export const useSessionStore = defineStore("session", () => {
  const token = ref(null);
  const role = ref(null);

  const setSession = (accessToken) => {
    token.value = accessToken;
    const payload = JSON.parse(atob(accessToken.split(".")[1]));
    console.log("payload", payload);
    role.value = payload.sub.role;
    localStorage.setItem("token", accessToken);
  };

  const clearSession = () => {
    token.value = null;
    role.value = null;
    localStorage.removeItem("token");
  };

  const loadSessionFromStorage = () => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setSession(savedToken);
    }
  };

  return {
    token,
    role,
    setSession,
    clearSession,
    loadSessionFromStorage,
  };
});
