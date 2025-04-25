<template>
    <button @click="logout">Logout</button>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { useSessionStore } from '../store/session';
  
  const router = useRouter();
  const session = useSessionStore();
  
  const logout = () => {
    session.clearSession();
    router.push('/');
  };
  </script>
  