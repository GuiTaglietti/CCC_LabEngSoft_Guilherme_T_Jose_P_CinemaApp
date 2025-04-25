<template>
    <div>
      <h1>Bem-vindo, {{ session.username }} ({{ session.role }})</h1>
      <LogoutButton />
    </div>
  </template>
  
  <script setup>
  import { useSessionStore } from '../store/session';
  import LogoutButton from '../components/LogoutButton.vue';
  
  const session = useSessionStore();
  </script>
  