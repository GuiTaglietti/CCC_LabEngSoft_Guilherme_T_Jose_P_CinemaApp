<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "./store/session";

const router = useRouter();
const session = useSessionStore();

onMounted(() => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (token && role) {
    session.setToken(token);
    session.setRole(role);

    if (role === "gerente") {
      router.push("/gerente");
    } else if (role === "usuario") {
      router.push("/usuario");
    }
  } else {
    router.push("/");
  }
});
</script>

<template>
  <router-view />
</template>

<style scoped>
</style>
