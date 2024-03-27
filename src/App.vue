<template>
  <router-view />
</template>

<script setup>
import { getAuth, onAuthStateChanged } from 'firebase/auth'

import { useAuthStore } from '@/store/auth'

const auth = getAuth()
const authStore = useAuthStore()

onAuthStateChanged(auth, async (user) => {
  if (user) {
    authStore.set(user)
  } else {
    authStore.$reset()
  }
})
</script>
