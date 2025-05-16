<template>
  <button class="logout-button" @click="logout">
    <i class="bi bi-box-arrow-right"></i>
    Logout
  </button>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useSessionStore } from "../store/session";

const router = useRouter();
const session = useSessionStore();

const logout = () => {
  session.clearSession();
  router.push("/login");
};
</script>

<style scoped>
@import "bootstrap-icons/font/bootstrap-icons.css";

.logout-button {
  background-color: #ff0000;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 0 10px red;
  transition: box-shadow 0.3s ease, transform 0.2s ease;
}

.logout-button:hover {
  box-shadow: 0 0 20px red;
  transform: scale(1.05);
}
</style>
