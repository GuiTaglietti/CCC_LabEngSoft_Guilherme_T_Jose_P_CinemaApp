<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "./store/session";

const router = useRouter();
const session = useSessionStore();

onMounted(() => {
  session.loadSessionFromStorage();

  if (session.token && session.role) {
    if (session.role === "gerente") {
      router.push("/gerente");
    } else if (session.role === "usuario") {
      router.push("/usuario");
    }
  } else {
    router.push("/login");
  }
});
</script>

<template>
  <router-view />
</template>

<style scoped></style>
