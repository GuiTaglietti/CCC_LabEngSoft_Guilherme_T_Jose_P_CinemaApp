<template>
    <div>
      <h1>Bem-vindo, {{ session.username }} ({{ session.role }})</h1>
      <LogoutButton />
    </div>
  </template>
  
<script setup>
import { useSessionStore } from '../store/session';
import { useRouter } from 'vue-router';

const session = useSessionStore();
const router = useRouter();

if (session.role !== 'gerente') {
  router.push('/');
}
</script>
